"""
One Hop Tests (core tests extracted
from the legacy SRI_Testing project)
"""
import sys
from typing import Optional, Dict
from json import dump
import asyncio

from reasoner_validator.trapi import TRAPISchemaValidator
from reasoner_validator.validator import TRAPIResponseValidator
from graph_validation_tests import (
    GraphValidationTest,
    TestCaseRun,
    get_parameters
)
from graph_validation_tests.translator.trapi import run_trapi_query
from graph_validation_tests.utils.unit_test_templates import (
    by_subject,
    inverse_by_new_subject,
    by_object,
    raise_subject_entity,
    raise_object_entity,
    raise_object_by_subject,
    raise_predicate_by_subject
)
import logging
logger = logging.getLogger(__name__)


class OneHopTestCaseRun(TestCaseRun):

    async def run_test_case(self):
        """
        Method to execute a TRAPI lookup, using a 'test' code template
        that defines a single TestCase using the GraphValidationTest associated TestAsset.
        :return: None, results are captured as validation messages within the TestCaseRun parent.
        """
        output_element: Optional[str]
        output_node_binding: Optional[str]

        # TODO: not sure if this is necessary - is the remapping
        #       of test asset fields already accomplished elsewhere?
        test_asset = self.translate_test_asset()

        trapi_request, output_element, output_node_binding = self.test(test_asset)

        if not trapi_request:
            # output_element and output_node_binding were
            # expropriated by the 'creator' to return error information
            context = output_element.split("|")
            self.report(
                code="skipped.test",
                identifier=context[0],
                context=context[1],
                reason=output_node_binding
            )

        else:
            # sanity check: verify first that the TRAPI request is well-formed by the creator(case)
            self.validate(trapi_request, component="Query")
            if not self.has_messages():

                # if no messages are reported, then continue with the validation

                # TODO: this is SRI_Testing harness functionality which we don't yet support here?
                #
                # if 'ara_source' in _test_asset and _test_asset['ara_source']:
                #     # sanity check!
                #     assert 'kp_source' in test_asset and test_asset['kp_source']
                #
                #     # Here, we need annotate the TRAPI request query graph to
                #     # constrain an ARA query to the test case specified 'kp_source'
                #     trapi_request = constrain_trapi_request_to_kp(
                #         trapi_request=trapi_request, kp_source=test_asset['kp_source']
                #     )

                # Capture the raw TRAPI query request for reporting
                self.trapi_request = trapi_request

                # Make the TRAPI call to the TestCase targeted ARS, KP or
                # ARA resource, using the case-documented input test edge
                trapi_response: Optional[Dict] = await run_trapi_query(
                    trapi_request=trapi_request,
                    component=self.get_component(),
                    environment=self.get_environment(),
                    target_trapi_version=self.trapi_version,
                    target_biolink_version=self.biolink_version
                )

                if not trapi_response:
                    self.report(code="error.trapi.response.empty")

                else:
                    # Capture the raw TRAPI query response for reporting
                    self.trapi_response = trapi_response

                    # Second sanity check: check whether the web service (HTTP) call itself was successful?
                    status_code: int = trapi_response['status_code']
                    if status_code != 200:
                        self.report("critical.trapi.response.unexpected_http_code", identifier=status_code)
                    else:
                        #########################################################
                        # Looks good so far, so now validate the TRAPI response #
                        #########################################################
                        response: Optional[Dict] = trapi_response['response_json']

                        if response:
                            # Report 'trapi_version' and 'biolink_version' recorded
                            # in the 'response_json' (if the tags are provided)
                            if 'schema_version' not in response:
                                self.report(code="warning.trapi.response.schema_version.missing")
                            else:
                                trapi_version: str = response['schema_version'] \
                                    if not self.trapi_version else self.trapi_version
                                logger.debug(
                                    f"run_one_hop_unit_test() using TRAPI version: '{trapi_version}'"
                                )

                            if 'biolink_version' not in response:
                                self.report(code="warning.trapi.response.biolink_version.missing")
                            else:
                                biolink_version = response['biolink_version'] \
                                    if not self.biolink_version else self.biolink_version
                                logger.debug(
                                    f"run_one_hop_unit_test() using Biolink Model version: '{biolink_version}'"
                                )

                            # If nothing badly wrong with the TRAPI Response to this point, then we also check
                            # whether the test input edge was returned in the Response Message knowledge graph
                            #
                            # case: Dict contains something like:
                            #
                            #     idx: 0,
                            #     subject_category: 'biolink:SmallMolecule',
                            #     object_category: 'biolink:Disease',
                            #     predicate: 'biolink:treats',
                            #     subject_id: 'CHEBI:3002',  # may have the deprecated key 'subject' here
                            #     object_id: 'MESH:D001249', # may have the deprecated key 'object' here
                            #
                            # the contents for which ought to be returned in
                            # the TRAPI Knowledge Graph, as a Result mapping?
                            self.case_input_found_in_response(test_asset, response)
                        else:
                            self.report(code="error.trapi.response.empty")


class OneHopTest(GraphValidationTest):
    def test_case_wrapper(self, test, **kwargs) -> TestCaseRun:
        return OneHopTestCaseRun(test_run=self, test=test, **kwargs)


async def run_one_hop_tests(**kwargs) -> Dict:
    # TRAPI test case query generators
    # used for OneHopTest runs
    trapi_generators = [
        by_subject,
        inverse_by_new_subject,
        by_object,
        raise_subject_entity,
        raise_object_entity,
        raise_object_by_subject,
        raise_predicate_by_subject
    ]
    results: Dict = await OneHopTest.run_tests(trapi_generators=trapi_generators, **kwargs)
    return results


def main():
    args = get_parameters(tool_name="One Hop Test of Knowledge Graph Navigation")
    results: Dict = asyncio.run(run_one_hop_tests(**vars(args)))
    # TODO: need to save these results somewhere central?
    dump(results, sys.stdout)


if __name__ == '__main__':
    main()
