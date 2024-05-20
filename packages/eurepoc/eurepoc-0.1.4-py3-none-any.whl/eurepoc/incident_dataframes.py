import pandas as pd
from eurepoc.tables import (
    model_to_dataframe, process_main_data, process_inclusion_criteria, process_source_disclosure_data,
    process_incident_type_data, process_receivers_data, process_attributions_data, process_attributions_bases_data,
    process_attributions_types_data, process_attribution_countries_data, process_attribution_actors_data,
    process_attribution_companies_data, process_attribution_legal_references_data, process_initiators_data,
    process_initiators_categories_data, process_cyber_conflict_issues_data, process_offline_conflict_issues_data,
    process_offline_conflict_intensities_data, process_political_responses_data, process_political_responses_type_data,
    process_technical_codings_data, process_cyber_intensity_data, process_mitre_initial_access_data,
    process_mitre_impact_data, process_impact_indicator_data, process_legal_codings_data,
    process_il_breach_indicator_data, process_legal_responses_data, process_legal_responses_type_data,
    process_source_urls_data, process_source_names_data, process_sources_attributions_data, clean_initiators
)


class IncidentDataFrameGenerator:
    """
    A class used for returning pandas DataFrames for specific variables/aspects of the incident to enable analysis.
    The different dfs can subsequently be joined through the `incident_id` column. Refer to the EuRepoC Codebook
    for more information about the substantive meaning of each variable (i.e. df column).

    Parameters:
        incident_data (list): List of incident data dictionaries, retrieved by using the `execute_query()` method of the
        `DatabaseQuery` class.

    Note
    ----------
    The data within the returned dfs are "exploded" over multiple rows for variables that contain multiple
    possible values. When performing analyses with pandas counting numbers of incidents, remember to use
    the `nunique()` method instead of the `count()` method.
    """
    def __init__(self, incident_data=None):
        self.data = incident_data

    def get_main_data(self):
        """Columns: incident_id, name, description, added_to_db, start_date, end_date, operation_type, status, updated_at,
        number_attributions, number_political_responses, number_legal_responses, casualties"""
        return model_to_dataframe(process_main_data(self.data))

    def get_inclusion_criteria(self):
        """Columns: incident_id, inclusion_criterion, inclusion_criterion_subcode"""
        return model_to_dataframe(process_inclusion_criteria(self.data))

    def get_sources_of_disclosure(self):
        """Columns: incident_id, source_disclosure"""
        return model_to_dataframe(process_source_disclosure_data(self.data))

    def get_operation_types(self):
        """Columns: incident_id, operation_type"""
        operation_types = []
        for incident in self.data:
            incident_dict = {
                'incident_id': incident['id'],
                'operation_type': incident['incident_type_clean'],
            }
            operation_types.append(incident_dict)
        return pd.DataFrame(operation_types)

    def get_incident_types(self):
        """Columns: incident_id, incident_type"""
        return model_to_dataframe(process_incident_type_data(self.data))

    def get_receivers(self):
        """Columns: receiver_id, incident_id, receiver_name, receiver_country, receiver_country_alpha_2_code, receiver_country_alpha_3_code,
        receiver_category, receiver_subcategory, receiver_regions (this is a list)"""
        return model_to_dataframe(process_receivers_data(self.data))

    def get_attributions(self):
        """Columns: attribution_id, incident_id, settled_attribution, attribution_date, attribution_updated_at,
        attribution_created_at, attribution_basis, attribution_type, attribution_subtype, attributing_country, attributing_actor,
        attributing_company, attribution_legal_reference, attribution_legal_reference_subcode, initiator_id,
        initiator_name, initiator_country, initiator_category, initiator_subcategory"""
        attributions_main = model_to_dataframe(process_attributions_data(self.data))
        attribution_bases = model_to_dataframe(process_attributions_bases_data(self.data))
        attribution_types = model_to_dataframe(process_attributions_types_data(self.data))
        attributing_country = model_to_dataframe(process_attribution_countries_data(self.data))
        attributing_actors = model_to_dataframe(process_attribution_actors_data(self.data))
        attributing_companies = model_to_dataframe(process_attribution_companies_data(self.data))
        attribution_legal_ref = model_to_dataframe(process_attribution_legal_references_data(self.data))
        attributions_df = attributions_main.merge(attribution_bases, on='attribution_id', how='outer')
        attributions_df = attributions_df.merge(attribution_types, on='attribution_id', how='outer')
        attributions_df = attributions_df.merge(attributing_country, on='attribution_id', how='outer')
        attributions_df = attributions_df.merge(attributing_actors, on='attribution_id', how='outer')
        attributions_df = attributions_df.merge(attributing_companies, on='attribution_id', how='outer')
        attributions_df = attributions_df.merge(attribution_legal_ref, on='attribution_id', how='outer')
        initiators_data = self.get_initiators(settled=False)
        attributions_df = attributions_df.merge(initiators_data, on='attribution_id', how='outer', suffixes=('', '_drop'))
        attributions_df = attributions_df.drop(columns=[col for col in attributions_df if col.endswith('_drop')])
        return attributions_df.drop_duplicates()

    def get_initiators(self, settled=True):
        """Columns: initiator_id, incident_id, attribution_id, settled_initiator, initiator_name,
        initiator_country, initiator_category, initiator_subcategory"""
        initiator_main = model_to_dataframe(process_initiators_data(self.data))
        initiator_categories = model_to_dataframe(process_initiators_categories_data(self.data))
        initiators_df = initiator_main.merge(initiator_categories, on='initiator_id', how='outer')
        return clean_initiators(initiators_df.drop_duplicates(), settled=settled)

    def get_cyber_conflict_issues(self):
        """Columns: incident_id, cyber_conflict_issue"""
        return model_to_dataframe(process_cyber_conflict_issues_data(self.data))

    def get_offline_conflicts(self):
        """Columns: incident_id, offline_conflict_issue, offline_conflict_name, offline_conflict_intensity,
        offline_conflict_intensity_subcode"""
        issues = model_to_dataframe(process_offline_conflict_issues_data(self.data))
        conflict_intensity = model_to_dataframe(process_offline_conflict_intensities_data(self.data))
        conflicts_df = issues.merge(conflict_intensity, on='incident_id', how='outer')
        return conflicts_df.drop_duplicates()

    def get_political_responses(self):
        """Columns: political_response_id, incident_id, political_response_date, political_response_responding_country,
        political_response_responding_actor, political_response_type, political_response_subtype"""
        pol_responses_main = model_to_dataframe(process_political_responses_data(self.data))
        pol_responses_type = model_to_dataframe(process_political_responses_type_data(self.data))
        pol_responses_df = pol_responses_main.merge(
            pol_responses_type,
            on='political_response_id',
            how='outer',
            suffixes=('', '_drop')
        )
        cleaned_df = pol_responses_df.drop_duplicates().drop(columns=[col for col in pol_responses_df if col.endswith('_drop')])
        return cleaned_df

    def get_technical_variables(self):
        """Columns: incident_id, zero_days, zero_days_subcode, has_disruption, user_interaction"""
        return model_to_dataframe(process_technical_codings_data(self.data))

    def get_cyber_intensity_variables(self):
        """Columns: incident_id, disruption, hijacking, data_theft, physical_effects_spatial, physical_effects_temporal,
        target_multiplier, unweighted_intensity, weighted_intensity"""
        return model_to_dataframe(process_cyber_intensity_data(self.data))

    def get_mitre_initial_access(self):
        """Columns: incident_id, mitre_initial_access"""
        return model_to_dataframe(process_mitre_initial_access_data(self.data))

    def get_mitre_impact(self):
        """Columns: incident_id, mitre_impact"""
        return model_to_dataframe(process_mitre_impact_data(self.data))

    def get_impact_indicator_variables(self):
        """Columns: incident_id, impact_indicator_score, impact_indicator_label, functional_impact, intelligence_impact,
        economic_impact, economic_impact_value, economic_impact_currency, affected_entities, affected_entities_value,
        affected_eu_countries, affected_eu_countries_value, affected_third_countries, affected_third_countries_value"""
        return model_to_dataframe(process_impact_indicator_data(self.data))

    def get_legal_variables(self):
        """Columns: incident_id, state_responsibility_actor, evidence_for_sanctions_indicator, response_indicator"""
        return model_to_dataframe(process_legal_codings_data(self.data))

    def get_il_breach_indicator(self):
        """Columns: incident_id, il_breach_indicator, il_breach_indicator_subcode"""
        return model_to_dataframe(process_il_breach_indicator_data(self.data))

    def get_legal_responses(self):
        """Columns: legal_response_id, incident_id, legal_response_date, legal_response_responding_country,
        legal_response_responding_actor, legal_response_type, legal_response_subtype"""
        leg_responses_main = model_to_dataframe(process_legal_responses_data(self.data))
        leg_responses_type = model_to_dataframe(process_legal_responses_type_data(self.data))
        leg_responses_df = leg_responses_main.merge(
            leg_responses_type,
            on='legal_response_id',
            how='outer',
            suffixes=('', '_drop')
        )
        cleaned_df = leg_responses_df.drop_duplicates().drop(columns=[col for col in leg_responses_df if col.endswith('_drop')])
        return cleaned_df

    def get_sources_urls(self):
        """Columns: source_urls_id, incident_id, source_url"""
        return model_to_dataframe(process_source_urls_data(self.data))

    def get_source_names(self):
        """Columns: source_url_id, incident_id, source_name"""
        return model_to_dataframe(process_source_names_data(self.data))

    def get_attribution_sources(self):
        """Columns: incident_id, attribution_source_url"""
        return model_to_dataframe(process_sources_attributions_data(self.data))
