from datetime import datetime
import pandas as pd
from eurepoc.table_models import (
    MainData, InclusionCriteria, SourceDisclosure, IncidentType, Receiver, Attributions,
    AttributionBases, AttributionTypes, AttributionCountries, AttributionActors, AttributionCompanies,
    AttributionLegalReferences, Initiators, InitiatorsCategories, CyberConflictIssues, OfflineConflictIssues,
    OfflineConflictIntensities, PoliticalResponses, PoliticalResponseTypes, TechnicalCodings, CyberIntensity,
    MitreInitialAccess, MitreImpact, ImpactIndicator, LegalCodings, ILBreachIndicator, LegalResponses,
    LegalResponseTypes, SourceUrls, SourceNames, SourceCategories, AttributionSources
)

# All functions in this file, retreive the variables from the list of incident dictionaries obtained by running the
# .execute_query() method from the DatabaseQuery class and return a list of objects of the respective table model. These are
# then used to create the dataframes in the IncidentDataFrameGenerator class.

def parse_date(date_str):
    """Parses a date string to a datetime object, returns None if input is None."""
    return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str and date_str != "Not available" else None


def process_main_data(full_data):
    return [
        MainData(
            incident_id=int(incident["id"]),
            name=incident["name"],
            description=incident["description"],
            added_to_db=parse_date(incident["added_to_DB"]),
            start_date=parse_date(incident["start_date"]),
            end_date=parse_date(incident["end_date"]),
            operation_type=incident["incident_type_clean"],
            status=incident["status"],
            updated_at=parse_date(incident["updated_at"]),
            number_attributions=int(incident["number_of_attributions"]),
            number_political_responses=int(incident["number_of_political_responses"]),
            number_legal_responses=int(incident["number_of_legal_responses"]),
            casualties=incident["casualties"][0]
        ) for incident in full_data
    ]


def process_inclusion_criteria(full_data):
    inclusion_criteria = []
    for incident in full_data:
        for criterion, subcode in zip(incident["inclusion_criteria"], incident["inclusion_criteria_subcode"]):
            inclusion_criteria.append(
                InclusionCriteria(
                    incident_id=int(incident["id"]),
                    inclusion_criterion=criterion,
                    inclusion_criterion_subcode=subcode
                )
            )
    return inclusion_criteria


def process_source_disclosure_data(full_data):
    source_disclosure_data = []
    for incident in full_data:
        for i in range(len(incident["source_incident_detection_disclosure"])):
            source_disclosure_data.append(
                SourceDisclosure(
                    incident_id=int(incident["id"]),
                    source_disclosure=incident["source_incident_detection_disclosure"][i],
                )
            )
    return source_disclosure_data


def process_incident_type_data(full_data):
    type_data = []
    for incident in full_data:
        for i in range(len(incident["incident_type"])):
            type_data.append(
                IncidentType(
                    incident_id=int(incident["id"]),
                    incident_type=incident["incident_type"][i],
                )
            )
    return type_data


def process_receivers_data(full_data):
    receivers_data = []
    for incident in full_data:
        for i in range(len(incident["receivers"])):
            if isinstance(incident["receivers"][i], dict):
                for j in range(len(incident["receivers"][i]['receiver_category'])):
                    receivers_data.append(
                        Receiver(
                            receiver_id=str(incident["receivers"][i]['receiver_id']) + f"_{j}",
                            incident_id=int(incident["id"]),
                            receiver_name=incident["receivers"][i]['receiver_name'],
                            receiver_category=incident["receivers"][i]['receiver_category'][j],
                            receiver_subcategory=incident["receivers"][i]['receiver_category_subcode'][j],
                            receiver_country=incident["receivers"][i]['receiver_country'],
                            receiver_country_alpha_2_code=incident["receivers"][i]['receiver_country_alpha_2_code'],
                            receiver_country_alpha_3_code=incident["receivers"][i]['receiver_country_alpha_3_code'],
                            receiver_regions=incident["receivers"][i]['receiver_regions']
                        )
                    )
            else:
                receivers_data.append(
                    Receiver(
                        incident_id=int(incident["id"]),
                        receiver_id=str(incident["id"]) + "_rec",
                        receiver_name=incident["receivers"][i],
                        receiver_country=None,
                        receiver_country_alpha_2_code=None,
                        receiver_country_alpha_3_code=None,
                        receiver_category=None,
                        receiver_subcategory=None,
                        receiver_regions=None
                    )
                )
    return receivers_data


def process_attributions_data(full_data):
    attributions_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                attributions_data.append(
                    Attributions(
                        attribution_id=str(incident["attributions"][i]['attribution_id']),
                        incident_id=int(incident["id"]),
                        settled_attribution=incident["attributions"][i]['settled'],
                        attribution_date=incident["attributions"][i]['attribution_full_date'][0] if incident["attributions"][i]['attribution_full_date'][0] != "Not available" else None
                    )
                )
            else:
                attributions_data.append(
                    Attributions(
                        attribution_id=str(incident["id"]) + "_attr",
                        incident_id=int(incident["id"]),
                        settled_attribution=None,
                        attribution_date=None
                    )
                )

    return attributions_data


def process_attributions_bases_data(full_data):
    attribution_bases_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                for j in range(len(incident["attributions"][i]['attribution_basis'])):
                    attribution_bases_data.append(
                        AttributionBases(
                            attribution_id=str(incident["attributions"][i]['attribution_id']),
                            attribution_basis=incident["attributions"][i]['attribution_basis'][j]
                        )
                    )

            else:
                attribution_bases_data.append(
                    AttributionBases(
                        attribution_id=str(incident["id"]) + "_attr",
                        attribution_basis=None
                    )
                )

    return attribution_bases_data


def process_attributions_types_data(full_data):
    attribution_types_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                for j in range(len(incident["attributions"][i]['attribution_type'])):
                    attribution_types_data.append(
                        AttributionTypes(
                            attribution_id=str(incident["attributions"][i]['attribution_id']),
                            attribution_type=incident["attributions"][i]['attribution_type'][j],
                            attribution_subtype=incident["attributions"][i]['attribution_type_subcode'][j]
                        )
                    )
            else:
                attribution_types_data.append(
                    AttributionTypes(
                        attribution_id=str(incident["id"]) + "_attr",
                        attribution_type=None,
                        attribution_subtype=None
                    )
                )

    return attribution_types_data


def process_attribution_countries_data(full_data):
    attribution_countries_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                for j in range(len(incident["attributions"][i]['attributing_country'])):
                    attribution_countries_data.append(
                        AttributionCountries(
                            attribution_id=str(incident["attributions"][i]['attribution_id']),
                            attributing_country=incident["attributions"][i]['attributing_country'][j]
                        )
                    )
            else:
                attribution_countries_data.append(
                    AttributionCountries(
                        attribution_id=str(incident["id"]) + "_attr",
                        attributing_country=None
                    )
                )

    return attribution_countries_data


def process_attribution_actors_data(full_data):
    attribution_actors_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                for j in range(len(incident["attributions"][i]['attributing_actor'])):
                    attribution_actors_data.append(
                        AttributionActors(
                            attribution_id=str(incident["attributions"][i]['attribution_id']),
                            attributing_actor=incident["attributions"][i]['attributing_actor'][j]
                        )
                    )
            else:
                attribution_actors_data.append(
                    AttributionActors(
                        attribution_id=str(incident["id"]) + "_attr",
                        attributing_actor=None
                    )
                )

    return attribution_actors_data


def process_attribution_companies_data(full_data):
    attribution_companies_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                for j in range(len(incident["attributions"][i]['attribution_it_company'])):
                    attribution_companies_data.append(
                        AttributionCompanies(
                            attribution_id=str(incident["attributions"][i]['attribution_id']),
                            attributing_company=incident["attributions"][i]['attribution_it_company'][j]
                        )
                    )
            else:
                attribution_companies_data.append(
                    AttributionCompanies(
                        attribution_id=str(incident["id"]) + "_attr",
                        attributing_company=None
                    )
                )

    return attribution_companies_data


def process_attribution_legal_references_data(full_data):
    attribution_legal_references_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                for j in range(len(incident["attributions"][i]['legal_attribution_reference'])):
                    attribution_legal_references_data.append(
                        AttributionLegalReferences(
                            attribution_id=str(incident["attributions"][i]['attribution_id']),
                            attribution_legal_reference=incident["attributions"][i]['legal_attribution_reference'][j],
                            attribution_legal_reference_subcode=incident["attributions"][i]['legal_attribution_reference_subcode'][j]
                        )
                    )
            else:
                attribution_legal_references_data.append(
                    AttributionLegalReferences(
                        attribution_id=str(incident["id"]) + "_attr",
                        attribution_legal_reference=None,
                        attribution_legal_reference_subcode=None
                    )
                )

    return attribution_legal_references_data


def process_initiators_data(full_data):
    initiators_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                initiators_data.append(
                    Initiators(
                        initiator_id="init_" + str(incident["id"]) + "_" + str(i),
                        incident_id=int(incident["id"]),
                        attribution_id=str(incident["attributions"][i]['attribution_id']),
                        settled_initiator=incident["attributions"][i]['settled'],
                        initiator_name=incident["attributions"][i]['attributed_initiator_name'][0],
                        initiator_country=incident["attributions"][i]['attributed_initiator_country'][0],
                    )
                )
            else:
                initiators_data.append(
                    Initiators(
                        initiator_id="init_" + str(incident["id"]) + "_" + str(i),
                        incident_id=int(incident["id"]),
                        attribution_id=str(incident["id"]) + "_attr",
                        settled_initiator=None,
                        initiator_name=None,
                        initiator_country=None
                    )
                )
    return initiators_data


def process_initiators_categories_data(full_data):
    initiators_categories_data = []
    for incident in full_data:
        for i in range(len(incident["attributions"])):
            if isinstance(incident["attributions"][i], dict):
                for j in range(len(incident["attributions"][i]['attributed_initiator_category'])):
                    initiators_categories_data.append(
                        InitiatorsCategories(
                            initiator_id="init_" + str(incident["id"]) + "_" + str(i),
                            initiator_category=incident["attributions"][i]['attributed_initiator_category'][j],
                            initiator_subcategory=incident["attributions"][i]['attributed_initiator_category_subcode'][j]
                        )
                    )
            else:
                initiators_categories_data.append(
                    InitiatorsCategories(
                        initiator_id="init_" + str(incident["id"]) + "_" + str(i),
                        initiator_category=None,
                        initiator_subcategory=None
                    )
                )

    return initiators_categories_data


def clean_initiators(initiators_df, settled=True):
    df = initiators_df.copy()
    df.loc[:, "initiator_country_clean"] = df["initiator_country"]

    def clean_initiator(row):
        if row["initiator_name"] in ["", "None", "Not available", "Unknown", None] and \
                row["initiator_country"] in ["Unknown", "Not available", None] and \
                row["initiator_category"] in ["Unknown - not attributed", "Not available", "Unknown", None]:
            row["initiator_country_clean"] = "Not attributed"
        return row

    df = df.apply(clean_initiator, axis=1)

    df["initiator_category"] = df.apply(
        lambda row: "Not attributed" if row["initiator_country_clean"] == "Not attributed" else row[
            "initiator_category"],
        axis=1
    )
    df["initiator_category"] = df["initiator_category"].replace(
        "Unknown - not attributed", "Unknown"
    )
    df["initiator_country_clean"] = df["initiator_country_clean"].replace(
        "Not available", "Unknown"
    )
    df["initiator_name"] = df.apply(
        lambda row: "Not attributed" if row["initiator_country_clean"] == "Not attributed" else row[
            "initiator_name"],
        axis=1
    )
    df["initiator_name"] = df["initiator_name"].replace(
        "Not available", "Unknown"
    )
    df["initiator_name"] = df["initiator_name"].fillna("Unknown")
    df["initiator_category"] = df["initiator_category"].replace(
        "Non-state actor, state-affiliation suggested", "State affiliated actor"
    )
    df["initiator_category"] = df.apply(
        lambda row: "Not attributed" if
        row["initiator_country_clean"] == "Unknown" and row["initiator_name"] == "Unknown" and
        row["initiator_category"] == "Not available" else row["initiator_category"], axis=1
    )
    df["initiator_category"] = df["initiator_category"].replace("Not available", "Unknown")
    df["initiator_category"] = df["initiator_category"].fillna("Not attributed")
    df["initiator_country_clean"] = df["initiator_country_clean"].fillna("Not attributed")
    df["initiator_country_clean"] = df.apply(
        lambda row: "Not attributed" if
        row["initiator_country_clean"] == "Unknown" and row["initiator_name"] == "Unknown"
        and row["initiator_category"] == "Not attributed" else row["initiator_country_clean"], axis=1
    )
    if settled:
        df = df[df["settled_initiator"] == True]
        df = df.drop(columns=["settled_initiator"])

    return df.drop(columns=["initiator_country"]).rename(columns={"initiator_country_clean": "initiator_country"})


def process_cyber_conflict_issues_data(full_data):
    cyber_conflict_issues_data = []
    for incident in full_data:
        for i in range(len(incident['cyber_conflict_issue'])):
            cyber_conflict_issues_data.append(
                CyberConflictIssues(
                    incident_id=int(incident["id"]),
                    cyber_conflict_issue=incident['cyber_conflict_issue'][i]
                )
            )
    return cyber_conflict_issues_data


def process_offline_conflict_issues_data(full_data):
    offline_conflict_issues_data = []
    for incident in full_data:
        for i in range(len(incident['offline_conflict_issue'])):
            offline_conflict_issues_data.append(
                OfflineConflictIssues(
                    incident_id=int(incident["id"]),
                    offline_conflict_issue=incident['offline_conflict_issue'][i],
                    offline_conflict_name=incident['offline_conflict_issue_subcode'][i]
                )
            )
    return offline_conflict_issues_data


def process_offline_conflict_intensities_data(full_data):
    offline_conflict_intensities_data = []
    for incident in full_data:
        for i in range(len(incident['offline_conflict_intensity'])):
            offline_conflict_intensities_data.append(
                OfflineConflictIntensities(
                    incident_id=int(incident["id"]),
                    offline_conflict_intensity=incident['offline_conflict_intensity'][i],
                    offline_conflict_intensity_subcode=incident['offline_conflict_intensity_subcode'][i]
                )
            )
    return offline_conflict_intensities_data


def process_political_responses_data(full_data):
    political_responses_data = []
    for incident in full_data:
        for i in range(len(incident['political_responses'])):
            if isinstance(incident['political_responses'][i], dict):
                political_responses_data.append(
                    PoliticalResponses(
                        political_response_id=str(incident['political_responses'][i]['political_response_id']),
                        incident_id=int(incident["id"]),
                        political_response_responding_country=incident['political_responses'][i]['political_response_country'][0],
                        political_response_responding_actor=incident['political_responses'][i]['political_response_actor'][0],
                        political_response_date=incident["political_responses"][i]['political_response_full_date'][0] if incident["political_responses"][i]['political_response_full_date'] != "Not available" else None
                    )
                )
            else:
                political_responses_data.append(
                    PoliticalResponses(
                        political_response_id=str(incident["id"]) + "_polres",
                        incident_id=int(incident["id"]),
                        political_response_responding_country=None,
                        political_response_responding_actor=None,
                        political_response_date=None
                    )
                )
    return political_responses_data


def process_political_responses_type_data(full_data):
    political_responses_type_data = []
    for incident in full_data:
        for i in range(len(incident['political_responses'])):
            if isinstance(incident['political_responses'][i], dict):
                for j in range(len(incident['political_responses'][i]['political_response_type'])):
                    political_responses_type_data.append(
                        PoliticalResponseTypes(
                            political_response_id=str(incident['political_responses'][i]['political_response_id']),
                            incident_id=int(incident['id']),
                            political_response_type=incident['political_responses'][i]['political_response_type'][j],
                            political_response_subtype=incident['political_responses'][i]['political_response_type_sub'][j]
                        )
                    )
            else:
                political_responses_type_data.append(
                    PoliticalResponseTypes(
                        political_response_id=str(incident["id"]) + "_polres",
                        incident_id=int(incident['id']),
                        political_response_type=None,
                        political_response_subtype=None
                    )
                )

    return political_responses_type_data


def process_technical_codings_data(full_data):
    technical_codings_data = []
    for incident in full_data:
        technical_codings_data.append(
            TechnicalCodings(
                incident_id=int(incident["id"]),
                zero_days=incident["zero_days"][0],
                zero_days_subcode=incident["zero_days_subcode"][0],
                has_disruption=incident['has_disruption'],
                user_interaction=incident["user_interaction"][0]
            )
        )
    return technical_codings_data


def process_cyber_intensity_data(full_data):
    cyber_intensity_data = []
    for incident in full_data:
        cyber_intensity_data.append(
            CyberIntensity(
                incident_id=int(incident["id"]),
                disruption=incident["disruption"][0],
                hijacking=incident["hijacking"][0],
                data_theft=incident["data_theft"][0],
                physical_effects_spatial=incident["physical_effects_spatial"][0],
                physical_effects_temporal=incident["physical_effects_temporal"][0],
                target_multiplier=incident["target_multiplier"][0],
                unweighted_intensity=int(incident['unweighted_cyber_intensity']) if incident['unweighted_cyber_intensity'] != "Not available" else 0,
                weighted_intensity=int(incident['weighted_cyber_intensity']) if incident['weighted_cyber_intensity'] != "Not available" else 0
            )
        )
    return cyber_intensity_data


def process_mitre_initial_access_data(full_data):
    mitre_initial_access_data = []
    for incident in full_data:
        mitre_initial_access_data.append(
            MitreInitialAccess(
                incident_id=int(incident["id"]),
                mitre_initial_access=incident['MITRE_initial_access'][0]
            )
        )
    return mitre_initial_access_data


def process_mitre_impact_data(full_data):
    mitre_impact_data = []
    for incident in full_data:
        mitre_impact_data.append(
            MitreImpact(
                incident_id=int(incident["id"]),
                mitre_impact=incident['MITRE_impact'][0]
            )
        )
    return mitre_impact_data


def process_impact_indicator_data(full_data):
    impact_indicator_data = []
    for incident in full_data:
        impact_indicator_data.append(
            ImpactIndicator(
                incident_id=int(incident["id"]),
                impact_indicator_score=int(incident['impact_indicator_value']) if incident['impact_indicator_value'] != "Not available" else 0,
                impact_indicator_label=incident['impact_indicator'],
                functional_impact=incident['functional_impact'],
                intelligence_impact=incident['intelligence_impact'],
                economic_impact=incident['economic_impact'],
                economic_impact_value=int(incident['economic_impact_exact_value']) if incident['economic_impact_exact_value'] != "Not available" else 0,
                economic_impact_currency=incident['economic_impact_currency'],
                affected_entities=incident['political_impact_affected_entities'],
                affected_entities_value=int(incident['political_impact_affected_entities_exact_value']) if incident['political_impact_affected_entities_exact_value'] != "Not available" else 0,
                affected_third_countries=incident['political_impact_third_countries'],
                affected_third_countries_value=int(incident['political_impact_third_countries_exact_value']) if incident["political_impact_third_countries_exact_value"] != "Not available" else 0
            )
        )
    return impact_indicator_data


def process_legal_codings_data(full_data):
    legal_codings_data = []
    for incident in full_data:
        legal_codings_data.append(
            LegalCodings(
                incident_id=int(incident["id"]),
                state_responsibility_actor=incident['state_responsibility_indicator'][0],
                evidence_for_sanctions_indicator=incident['evidence_for_sanctions_indicator'][0],
                response_indicator=incident['legal_response_indicator'][0]
            )
        )
    return legal_codings_data


def process_il_breach_indicator_data(full_data):
    il_breach_indicator_data = []
    for incident in full_data:
        for i in range(len(incident['IL_breach_indicator'])):
            il_breach_indicator_data.append(
                ILBreachIndicator(
                    incident_id=int(incident["id"]),
                    il_breach_indicator=incident['IL_breach_indicator'][i],
                    il_breach_indicator_subcode=incident['IL_breach_indicator_subcode'][i]
                )
            )
    return il_breach_indicator_data


def process_legal_responses_data(full_data):
    legal_responses_data = []
    for incident in full_data:
        for i in range(len(incident['legal_responses'])):
            if isinstance(incident['legal_responses'][i], dict):
                legal_responses_data.append(
                    LegalResponses(
                        legal_response_id=str(incident['legal_responses'][i]['legal_response_id']),
                        incident_id=int(incident["id"]),
                        legal_response_responding_country=incident['legal_responses'][i]['legal_response_country'][0],
                        legal_response_responding_actor=incident['legal_responses'][i]['legal_response_actor'][0],
                        legal_response_date=incident["legal_responses"][i]['legal_response_full_date'][0] if incident["legal_responses"][i]['legal_response_full_date'] != "Not available" else None

                    )
                )
            else:
                legal_responses_data.append(
                    LegalResponses(
                        legal_response_id=str(incident["id"]) + "_legres",
                        incident_id=int(incident["id"]),
                        legal_response_responding_country=None,
                        legal_response_responding_actor=None,
                        legal_response_date=None
                    )
                )
    return legal_responses_data


def process_legal_responses_type_data(full_data):
    legal_responses_type_data = []
    for incident in full_data:
        for i in range(len(incident['legal_responses'])):
            if isinstance(incident['legal_responses'][i], dict):
                for j in range(len(incident['legal_responses'][i]['legal_response_type'])):
                    legal_responses_type_data.append(
                        LegalResponseTypes(
                            legal_response_id=str(incident['legal_responses'][i]['legal_response_id']),
                            incident_id=int(incident["id"]),
                            legal_response_type=incident['legal_responses'][i]['legal_response_type'][j],
                            legal_response_subtype=incident['legal_responses'][i]['legal_response_type_sub'][j]
                        )
                    )
            else:
                legal_responses_type_data.append(
                    LegalResponseTypes(
                        legal_response_id=str(incident["id"]) + "_legres",
                        incident_id=int(incident["id"]),
                        legal_response_type=None,
                        legal_response_subtype=None
                    )
                )

    return legal_responses_type_data


def process_source_urls_data(full_data):
    sources_url_data = []
    for incident in full_data:
        for i in range(len(incident['sources_url'])):
            sources_url_data.append(
                SourceUrls(
                    source_urls_id="source_" + str(incident["id"]) + "_" + str(i),
                    incident_id=int(incident["id"]),
                    source_url=incident['sources_url'][i],
                )
            )
    return sources_url_data


def process_source_names_data(full_data):
    sources_names_data = []
    for incident in full_data:
        for i in range(len(incident['sources_name'])):
            sources_names_data.append(
                SourceNames(
                    source_url_id="source_" + str(incident["id"]) + "_" + str(i),
                    incident_id=int(incident["id"]),
                    source_name=incident['sources_name'][i]
                )
            )
    return sources_names_data


def process_source_categories_data(full_data):
    sources_categories_data = []
    for incident in full_data:
        for i in range(len(incident['sources_name'])):
            sources_categories_data.append(
                SourceCategories(
                    source_url_id="source_" + str(incident["id"]) + "_" + str(i),
                    incident_id=int(incident["id"]),
                    source_category=incident['sources_category'][i]
                )
            )
    return sources_categories_data


def process_sources_attributions_data(full_data):
    sources_attributions_data = []
    for incident in full_data:
        for i in range(len(incident['sources_attribution'])):
            sources_attributions_data.append(
                AttributionSources(
                    incident_id=int(incident["id"]),
                    attribution_source_url=incident['sources_attribution'][i]
                )
            )
    return sources_attributions_data


def model_to_dataframe(models):
    data_dicts = [model.dict() for model in models]
    return pd.DataFrame(data_dicts)
