from datetime import datetime


def safe_get(d, *keys):
    """Safely get a value from a nested dictionary - dealing with None values and missing keys"""
    for key in keys:
        if d and isinstance(d, dict):
            d = d.get(key)
        else:
            return ""
    return d


def clean_incidents_dict(data):
    """Unnests the data output from the EuRepoC API and returns a cleaned version of the data."""
    clean_data = []
    for incident in data:
        incident_dic = {
            "id": "",
            "name": "",
            "description": "",
            "added_to_DB": "",
            "start_date": "",
            "end_date": "",
            "status": "",
            "updated_at": "",

            "inclusion_criteria": [],
            "inclusion_criteria_subcode": [],
            "source_incident_detection_disclosure": [],

            "incident_type": [],

            "receivers": [],

            "initiator_name": [],
            "initiator_country": [],
            "initiator_category": [],
            "initiator_category_subcode": [],

            "number_of_attributions": "",
            "attributions": [],
            "temporal_attribution_sequence": [],

            "cyber_conflict_issue": [],
            "offline_conflict_issue": [],
            "offline_conflict_issue_subcode": [],
            "offline_conflict_intensity": [],
            "offline_conflict_intensity_subcode": [],

            "number_of_political_responses": "",
            "political_responses": [],

            "zero_days": [],
            "zero_days_subcode": [],
            "MITRE_initial_access": [],
            "MITRE_impact": [],
            "user_interaction": [],

            "has_disruption": "",
            "data_theft": [],
            "disruption": [],
            "hijacking": [],
            "physical_effects_spatial": [],
            "physical_effects_temporal": [],
            "unweighted_cyber_intensity": "",
            "target_multiplier": [],
            "weighted_cyber_intensity": "",

            "impact_indicator": "",
            "impact_indicator_value": "",
            "functional_impact": "",
            "intelligence_impact": "",
            "political_impact_affected_entities": "",
            "political_impact_affected_entities_exact_value": "",
            "political_impact_eu_countries": "",
            "political_impact_eu_countries_exact_value": "",
            "political_impact_third_countries": "",
            "political_impact_third_countries_exact_value": "",
            "economic_impact": "",
            "economic_impact_exact_value": "",
            "economic_impact_currency": "",

            "state_responsibility_indicator": [],
            "IL_breach_indicator": [],
            "IL_breach_indicator_subcode": [],
            "evidence_for_sanctions_indicator": [],

            "number_of_legal_responses": "",
            "legal_responses": [],

            "legal_attribution_reference": [],
            "legal_attribution_reference_subcode": [],

            "legal_response_indicator": [],

            "casualties": [],

            "sources_name": [],
            "sources_category": [],
            "sources_url": [],
            "sources_attribution": [],
            "link_incident_EuRepoC": "",
            "logs": [],
            "articles": []
        }

        incident_dic.update(id=incident["id"])
        incident_dic.update(name=incident["name"])
        incident_dic.update(description=incident["description"])
        incident_dic.update(status=incident["status"])
        incident_dic.update(updated_at=incident["updatedAt"].split("T")[0])

        if incident["start_date"] is None:
            incident_dic.update(start_date=incident["start_date"])
        else:
            incident_dic.update(start_date=incident["start_date"].split("T")[0])

        incident_dic.update(added_to_DB=incident["createdAt"].split("T")[0])
        incident_dic.update(link_incident_EuRepoC="https://database.eurepoc-dashboard.eu/?cyber_incident=" + str(incident["id"]))

        enddate_year = None
        enddate_month = None
        enddate_day = None
        if incident["end"] is not None:
            if incident["end"]["year"] is not None:
                enddate_year = int(incident["end"]["year"])
            if incident["end"]["month"] is not None:
                enddate_month = int(incident["end"]["month"])
            if incident["end"]["day"] is not None:
                enddate_day = int(incident["end"]["day"])

        if enddate_year is not None and enddate_year != 0 and enddate_month is not None and enddate_month != 0 \
                and enddate_day is not None and enddate_day != 0:
            incident_dic.update(end_date=f'{enddate_year}-{enddate_month:02d}-{enddate_day:02d}')
        else:
            incident_dic.update(end_date="Not available")

        incident_dic["logs"].append(incident["logs"])
        incident_dic["articles"].append(incident["articles"]["data"])

        for elem in incident["source_incident_detection_disclosure"]:
            incident_dic["source_incident_detection_disclosure"].append(safe_get(
                elem, "code", "data", "attributes", "title"))

        for elem in incident["inclusion_criteria"]:
            incident_dic["inclusion_criteria"].append(safe_get(elem, "code", "data", "attributes", "title"))
            incident_dic["inclusion_criteria_subcode"].append(safe_get(
                elem, "subcode", "data", "attributes", "title"))

        for elem in incident["temporal_attribution_sequence"]:
            incident_dic["temporal_attribution_sequence"].append(safe_get(
                elem, "code", "data", "attributes", "title"))

        for elem in incident["attributes"]:
            if elem is not None:
                if 'incident_type' in elem:
                    type_inc = elem["incident_type"]
                    for subelem in type_inc:
                        incident_dic["incident_type"].append(safe_get(
                            subelem, "code", "data", "attributes", "title"))

        i = 0
        for elem in incident.get("receiver", {}).get("data", []):
            receiver = {
                "receiver_id": "",
                "receiver_name": "",
                "receiver_country": "",
                "receiver_country_alpha_2_code": "",
                "receiver_country_alpha_3_code": "",
                "receiver_regions": [],
                "receiver_category": [],
                "receiver_category_subcode": [],
            }

            rec_id = elem["id"]
            receiver.update(receiver_id=rec_id)
            receiver.update(receiver_country=safe_get(
                elem, "attributes", "country", "data", "attributes", "name"))
            receiver.update(receiver_country_alpha_2_code=safe_get(
                elem, "attributes", "country", "data", "attributes", "alpha_2_code"
            ))
            receiver.update(receiver_country_alpha_3_code=safe_get(
                elem, "attributes", "country", "data", "attributes", "alpha_3_code"
            ))
            receiver.update(receiver_name=safe_get(elem, "attributes", "name"))

            region_list = safe_get(elem, "attributes", "country", "data", "attributes")
            if region_list != "":
                if len(region_list["country_regions"]) > 0:
                    for region in region_list["country_regions"]:
                        if region['to'] is None:
                            receiver["receiver_regions"].append(safe_get(region, "region", "data", "attributes", "name"))
                        else:
                            if incident["start_date"] is not None:
                                startdate = datetime.strptime(incident["start_date"], '%Y-%m-%d')
                                if startdate <= datetime.strptime('2020-01-31', '%Y-%m-%d'):
                                    receiver["receiver_regions"].append(safe_get(region, "region", "data", "attributes", "name"))

            for cat in elem.get("attributes", {}).get("category", []):
                receiver["receiver_category"].append(safe_get(cat, "code", "data", "attributes", "title"))
                receiver["receiver_category_subcode"].append(safe_get(cat, "subcode", "data", "attributes", "title"))

            incident_dic["receivers"].append(receiver)
            i += 1

        incident_dic.update(number_of_attributions=len(incident["attributions"]))
        for attribution in incident["attributions"]:
            if attribution["settled_attribution"] is True:
                for initiator in attribution.get("initiators", {}).get("data", []):
                    incident_dic["initiator_name"].append(safe_get(
                        initiator, "attributes", "name"))

                    for initiating_country in initiator.get("attributes", {}).get("countries", {}).get("data", []):
                        incident_dic["initiator_country"].append(safe_get(
                            initiating_country, "attributes", "name"))

                    for initiating_category in initiator.get("attributes", {}).get("category", []):
                        incident_dic["initiator_category"].append(safe_get(
                            initiating_category, "code", "data", "attributes", "title"))
                        incident_dic["initiator_category_subcode"].append(safe_get(
                            initiating_category, "subcode", "data", "attributes", "title"))

            attribution_dict = {
                "attribution_id": "",
                "settled": "",
                "attribution_year": "",
                "attribution_month": "",
                "attribution_day": "",
                "attribution_basis": [],
                "attribution_type": [],
                "attribution_type_subcode": [],
                "attributing_country": [],
                "attributing_actor": [],
                "attribution_it_company": [],
                "legal_attribution_reference": [],
                "legal_attribution_reference_subcode": [],
                "attributed_initiator_name": [],
                "attributed_initiator_country": [],
                "attributed_initiator_category": [],
                "attributed_initiator_category_subcode": [],
            }

            attribution_dict.update(attribution_id=attribution["id"])
            attribution_dict.update(settled=attribution["settled_attribution"])

            for basis in attribution.get("attribution_basis", []):
                attribution_dict["attribution_basis"].append(safe_get(
                    basis, "code", "data", "attributes", "title"))

            for type_inc in attribution.get("attribution_type", []):
                attribution_dict["attribution_type"].append(safe_get(
                    type_inc, "code", "data", "attributes", "title"))
                attribution_dict["attribution_type_subcode"].append(safe_get(
                    type_inc, "subcode", "data", "attributes", "title"))

            for att_country in attribution.get("attributing_country", {}).get("data", []):
                attribution_dict["attributing_country"].append(safe_get(
                    att_country, "attributes", "name"))

            for att_actor in attribution.get("attributing_actors", {}).get("data", []):
                attribution_dict["attributing_actor"].append(safe_get(
                    att_actor, "attributes", "name"))

            attr_year = None
            attr_month = None
            attr_day = None
            if attribution["attribution_date"] is not None:
                if attribution["attribution_date"]["year"] is not None:
                    attr_year = int(attribution["attribution_date"]["year"])
                if attribution["attribution_date"]["month"] is not None:
                    attr_month = int(attribution["attribution_date"]["month"])
                if attribution["attribution_date"]["day"] is not None:
                    attr_day = int(attribution["attribution_date"]["day"])
            attribution_dict.update(attribution_year=attr_year)
            attribution_dict.update(attribution_month=attr_month)
            attribution_dict.update(attribution_day=attr_day)

            for company in attribution.get("it_companies", {}).get("data", []):
                attribution_dict["attribution_it_company"].append(safe_get(
                    company, "attributes", "name"))

            for legal_attr in attribution.get("legal_attribution_references", []):
                attribution_dict["legal_attribution_reference"].append(safe_get(
                    legal_attr, "code", "data", "attributes", "title"))
                attribution_dict["legal_attribution_reference_subcode"].append(safe_get(
                    legal_attr, "subcode", "data", "attributes", "title"))

            for initiator in attribution.get("initiators", {}).get("data", []):
                attribution_dict["attributed_initiator_name"].append(safe_get(
                    initiator, "attributes", "name"))

                for initiating_country in initiator.get("attributes", {}).get("countries", {}).get("data", []):
                    attribution_dict["attributed_initiator_country"].append(safe_get(
                        initiating_country, "attributes", "name"))

                for initiating_category in initiator.get("attributes", {}).get("category", []):
                    attribution_dict["attributed_initiator_category"].append(safe_get(
                        initiating_category, "code", "data", "attributes", "title"))
                    attribution_dict["attributed_initiator_category_subcode"].append(safe_get(
                        initiating_category, "subcode", "data", "attributes", "title"))

            incident_dic["attributions"].append(attribution_dict)

        for elem in incident.get("attributes", []):
            if 'has_disruption' in elem:
                incident_dic.update(has_disruption=elem["has_disruption"])
            if 'data_theft' in elem:
                incident_dic["data_theft"].append(safe_get(
                    elem, "data_theft", "code", "data", "attributes", "title"))
            if "zero_days_used" in elem:
                incident_dic["zero_days"].append(safe_get(
                    elem, "zero_days_used", "code", "data", "attributes", "title"))
                incident_dic["zero_days_subcode"].append(safe_get(
                    elem, "zero_days_used", "subcode", "data", "attributes", "title"))
            if "weighted_cyber_intensity" in elem:
                incident_dic.update(weighted_cyber_intensity=safe_get(
                    elem, "weighted_cyber_intensity", "code", "data", "attributes", "code"))

            if "unweighted_cyber_intensity" in elem:
                incident_dic.update(unweighted_cyber_intensity=safe_get(
                    elem, "unweighted_cyber_intensity"))

            if "disruption" in elem:
                incident_dic["disruption"].append(safe_get(
                    elem, "disruption", "code", "data", "attributes", "title"))

            if "hijacking" in elem:
                incident_dic["hijacking"].append(safe_get(
                    elem, "hijacking", "code", "data", "attributes", "title"))

            if "cyber_conflict_issue" in elem:
                for subelem in elem.get("cyber_conflict_issue", []):
                    incident_dic["cyber_conflict_issue"].append(safe_get(
                        subelem, "code", "data", "attributes", "title"))

            if "offline_conflict_issue" in elem:
                for subelem in elem.get("offline_conflict_issue", []):
                    incident_dic["offline_conflict_issue"].append(safe_get(
                        subelem, "code", "data", "attributes", "title"))

            if "offline_conflict_issue" in elem:
                for subelem in elem.get("offline_conflict_issue", []):
                    incident_dic["offline_conflict_issue_subcode"].append(safe_get(
                        subelem, "subcode", "data", "attributes", "title"))

            if "offline_conflict_intensity" in elem:
                incident_dic["offline_conflict_intensity"].append(safe_get(
                    elem, "offline_conflict_intensity", "code", "data", "attributes", "title"))
                incident_dic["offline_conflict_intensity_subcode"].append(safe_get(
                    elem, "offline_conflict_intensity", "subcode", "data", "attributes", "title"))

            if "physical_effects_temporal" in elem:
                incident_dic["physical_effects_temporal"].append(safe_get(
                    elem, "physical_effects_temporal", "code", "data", "attributes", "title"))

            if "physical_effects_spatial" in elem:
                incident_dic["physical_effects_spatial"].append(safe_get(
                    elem, "physical_effects_spatial", "code", "data", "attributes", "title"))

            if "casualties" in elem:
                incident_dic["casualties"].append(safe_get(
                    elem, "casualties", "code", "data", "attributes", "title"))

            if "target_effect_multiplier" in elem:
                incident_dic["target_multiplier"].append(safe_get(
                    elem, "target_effect_multiplier", "code", "data", "attributes", "title"))

        for elem in incident.get("mitre_initial_access", []):
            incident_dic["MITRE_initial_access"].append(safe_get(
                elem, "code", "data", "attributes", "title"))

        for elem in incident.get("mitre_impact", []):
            incident_dic["MITRE_impact"].append(safe_get(
                elem, "code", "data", "attributes", "title"))

        incident_dic.update(number_of_political_responses=len(incident["political_response"]))

        if len(incident["political_response"]) > 0:
            for elem in incident["political_response"]:
                pol_response = {
                    "political_response_id": elem['id'],
                    "political_response_country": [],
                    "political_response_actor": [],
                    "political_response_type": [],
                    "political_response_type_sub": [],
                    "political_response_year": "",
                    "political_response_month": "",
                    "political_response_day": "",
                }

                for subelem in elem["countries"]["data"]:
                    pol_response["political_response_country"].append(safe_get(
                        subelem, "attributes", "name"))

                for subelem in elem.get("actors", {}).get("data", []):
                    pol_response["political_response_actor"].append(safe_get(
                        subelem, "attributes", "name"))

                if len(elem["date"]) == 0:
                    incident_dic.update(number_of_political_responses=incident_dic["number_of_political_responses"] - 1)
                for subelem in elem.get("date", {}):
                    if subelem["year"] is not None:
                        pol_response.update(political_response_year=subelem["year"])
                    if subelem["year"] == 0:
                        incident_dic.update(
                            number_of_political_responses=incident_dic["number_of_political_responses"] - 1)
                    if subelem["month"] is not None:
                        pol_response.update(political_response_month=subelem["month"])
                    if subelem["day"] is not None:
                        pol_response.update(political_response_day=subelem["day"])

                if len(elem["type"]) == 0:
                    pol_response["political_response_type"].append("NA")
                    pol_response["political_response_type_sub"].append("NA")
                else:
                    for subelem in elem.get("type", {}):
                        pol_response["political_response_type"].append(
                            safe_get(subelem, "code", "data", "attributes", "title"))
                        pol_response["political_response_type_sub"].append(
                            safe_get(subelem, "subcode", "data", "attributes", "title"))

                incident_dic["political_responses"].append(pol_response)

        if incident["user_interaction"] is not None:
            incident_dic["user_interaction"].append(safe_get(
                incident, "user_interaction", "code", "data", "attributes", "title"))

        if incident["state_responsibility_indicator"] is not None:
            incident_dic["state_responsibility_indicator"].append(safe_get(
                incident, "state_responsibility_indicator", "code", "data", "attributes", "title"))

        for elem in incident.get("il_breach_indicator", []):
            incident_dic["IL_breach_indicator"].append(safe_get(
                elem, "code", "data", "attributes", "title"))
            incident_dic["IL_breach_indicator_subcode"].append(safe_get(
                elem, "subcode", "data", "attributes", "title"))

        incident_dic.update(number_of_legal_responses=len(incident["legal_response"]))
        if len(incident["legal_response"]) > 0:
            for elem in incident["legal_response"]:
                legal_response = {
                    "legal_response_id": elem['id'],
                    "legal_response_country": [],
                    "legal_response_actor": [],
                    "legal_response_type": [],
                    "legal_response_type_sub": [],
                    "legal_response_year": "",
                    "legal_response_month": "",
                    "legal_response_day": "",
                }

                for subelem in elem.get("countries", {}).get("data", []):
                    legal_response["legal_response_country"].append(safe_get(
                        subelem, "attributes", "name"))

                for subelem in elem.get("actors", {}).get("data", []):
                    legal_response["legal_response_actor"].append(safe_get(
                        subelem, "attributes", "name"))

                if len(elem["date"]) == 0:
                    incident_dic.update(number_of_legal_responses=incident_dic["number_of_legal_responses"] - 1)
                for subelem in elem["date"]:
                    if subelem["year"] is not None:
                        legal_response.update(legal_response_year=subelem["year"])
                    if subelem["year"] == 0:
                        incident_dic.update(number_of_legal_responses=incident_dic["number_of_legal_responses"] - 1)
                    if subelem["month"] is not None:
                        legal_response.update(legal_response_month=subelem["month"])
                    if subelem["day"] is not None:
                        legal_response.update(legal_response_day=subelem["day"])

                for subelem in elem.get("type", {}):
                    legal_response["legal_response_type"].append(safe_get(
                        subelem, "code", "data", "attributes", "title"))
                    legal_response["legal_response_type_sub"].append(safe_get(
                        subelem, "subcode", "data", "attributes", "title"))

                incident_dic["legal_responses"].append(legal_response)

        if incident["response_indicator"] is not None:
            incident_dic["legal_response_indicator"].append(safe_get(
                incident, "response_indicator", "code", "data", "attributes", "title"))

        if incident["evidence_for_sanctions"] is not None:
            incident_dic["evidence_for_sanctions_indicator"].append(safe_get(
                incident, "evidence_for_sanctions", "code", "data", "attributes", "title"))

        if incident["impact_indicator"] is not None:
            incident_dic.update(impact_indicator_value=int(safe_get(
                incident, "impact_indicator", "impact_indicator", "value")))
            incident_dic.update(impact_indicator=safe_get(
                incident, "impact_indicator", "impact_indicator", "code", "code", "data", "attributes", "title"))

        if incident["impact_indicator"] is not None:
            incident_dic.update(functional_impact=safe_get(
                incident, "impact_indicator", "functional_impact", "code", "data", "attributes", "title"))

        if incident["impact_indicator"] is not None:
            incident_dic.update(intelligence_impact=safe_get(
                incident, "impact_indicator", "intelligence_impact", "code", "data", "attributes", "title"))

        if incident["impact_indicator"] is not None:
            incident_dic.update(
                political_impact_affected_entities_exact_value=safe_get(
                    incident, "impact_indicator", "political_impact", "value"))

            incident_dic.update(political_impact_affected_entities=safe_get(
                incident, "impact_indicator", "political_impact", "code", "code", "data", "attributes", "title"))

        if incident["impact_indicator"] is not None:
            incident_dic.update(political_impact_third_countries_exact_value=safe_get(
                incident, "impact_indicator", "political_impact_third_countries", "value"))
            incident_dic.update(political_impact_third_countries=safe_get(
                incident, "impact_indicator", "political_impact_third_countries", "code", "code", "data",
                "attributes", "title"))


        if incident["impact_indicator"] is not None:
            incident_dic.update(political_impact_eu_countries_exact_value=safe_get(
                incident, "impact_indicator", "political_impact_countries", "value"))
            incident_dic.update(political_impact_eu_countries=safe_get(
                incident, "impact_indicator", "political_impact_countries", "code", "code", "data",
                "attributes", "title"))


        if incident["impact_indicator"] is not None:
            incident_dic.update(economic_impact_exact_value=safe_get(
                incident, "impact_indicator", "economic_impact", "value"))
            incident_dic.update(economic_impact_currency=safe_get(
                incident, "impact_indicator", "economic_impact", "currency"))
            incident_dic.update(economic_impact=safe_get(
                incident, "impact_indicator", "economic_impact", "code", "code", "data", "attributes", "title"))

        for article in incident["articles"]["data"]:
            incident_dic["sources_url"].append(safe_get(article, "attributes", "url"))
            incident_dic["sources_name"].append(safe_get(article, "attributes", "source", "data", "attributes", "name"))
            incident_dic["sources_category"].append(safe_get(
                article, "attributes", "source", "data", "attributes", "category"))

        if incident["sources_attribution"]["data"] is not None:
            for source in incident["sources_attribution"]["data"]:
                incident_dic["sources_attribution"].append(safe_get(source, "attributes", "url"))

        if incident["temporal_attribution_sequence"] is not None:
            incident_dic.update(temporal_attribution_sequence=safe_get(
                incident, "temporal_attribution_sequence", "code", "data", "attributes", "title"))

        clean_data.append(incident_dic)

    return clean_data


def brexit_clean(data, receiver_region=None):
    """Excludes incidents when only the UK was targeted post-Brexit when the EU receiver_region filter is used."""
    filtered_data = []
    if receiver_region == "EU":
        for incident in data:
            if all(receiver["receiver_country"] == "United Kingdom" for receiver in incident["receivers"]):
                if incident["start_date"] is not None and datetime.strptime(incident["start_date"], '%Y-%m-%d') > datetime.strptime('2020-02-01', '%Y-%m-%d'):
                    continue
            filtered_data.append(incident)
        return filtered_data
    else:
        return data


def clean_receivers(data):
    """Changes the receiver_country value for EU and NATO institutions."""
    for incident in data:
        for receiver in incident["receivers"]:
            if receiver["receiver_country"] == "EU (region)" and "International / supranational organization" in receiver["receiver_category"]:
                receiver["receiver_country"] = "EU (institutions)"
    for incident in data:
        for receiver in incident["receivers"]:
            if receiver["receiver_country"] == "NATO (region)" and "International / supranational organization" in receiver["receiver_category"]:
                receiver["receiver_country"] = "NATO (institutions)"

    return data


def clean_dates(data):
    """Converts the year, month, and day values to a full date format for the attributions and political/legal responses"""
    for incident in data:
        if incident["number_of_attributions"] > 0:
            for attribution in incident["attributions"]:
                attribution_full_date = []
                year = attribution.get("attribution_year")
                month = attribution.get("attribution_month")
                day = attribution.get("attribution_day")
                if all(v is None for v in [year, month, day]):
                    attribution_full_date.append("Not available")
                elif year == 0:
                    attribution_full_date.append("Not available")
                elif month is None or month == 0:
                    attribution_full_date.append(str(year))
                elif day is None or day == 0:
                    attribution_full_date.append(f"{year}-{month}-01")
                else:
                    attribution_full_date.append(f"{year}-{month}-{day}")
                attribution["attribution_full_date"] = attribution_full_date

    for incident in data:
        if incident["number_of_political_responses"] > 0:
            for response in incident["political_responses"]:
                response_full_date = []
                year = response.get("political_response_year")
                month = response.get("political_response_month")
                day = response.get("political_response_day")
                if all(v is None for v in [year, month, day]):
                    response_full_date.append("Not available")
                elif year == 0:
                    response_full_date.append("Not available")
                elif month is None or month == 0:
                    response_full_date.append(str(year))
                elif day is None or day == 0:
                    response_full_date.append(f"{year}-{month}-01")
                else:
                    response_full_date.append(f"{year}-{month}-{day}")
                response["political_response_full_date"] = response_full_date
        else:
            for response in incident["political_responses"]:
                response["political_response_full_date"] = "Not available"

    for incident in data:
        if incident["number_of_legal_responses"] > 0:
            for response in incident["legal_responses"]:
                response_full_date = []
                year = response.get("legal_response_year")
                month = response.get("legal_response_month")
                day = response.get("legal_response_day")
                if all(v is None for v in [year, month, day]):
                    response_full_date.append("Not available")
                elif year == 0:
                    response_full_date.append("Not available")
                elif month is None or month == 0:
                    response_full_date.append(str(year))
                elif day is None or day == 0:
                    response_full_date.append(f"{year}-{month}-01")
                else:
                    response_full_date.append(f"{year}-{month}-{day}")
                response["legal_response_full_date"] = response_full_date
        else:
            for response in incident["legal_responses"]:
                response["legal_response_full_date"] = "Not available"

    return data


def replace_empty_strings(data):
    """Replaces empty strings with 'Not available' across the data for consistently handling missing values."""
    if isinstance(data, list):
        if len(data) == 0:
            return ["Not available"]
        return [replace_empty_strings(item) for item in data]
    elif isinstance(data, dict):
        return {k: replace_empty_strings(v) for k, v in data.items()}
    elif data == "":
        return "Not available"
    else:
        return data


def clean_types(data):
    """Adding a variable cleaning the incident types to a "one-level" category for more meaningful analyses."""
    def translate_type(types):
        types = [t for t in types if isinstance(t, str)]

        type_mapping = {
            "Disruption": "DDoS/Defacement",
            "Data theft": "Data theft",
            "Data theft & Doxing": "Hack and leak",
            "Ransomware": "Ransomware"
        }

        sorted_types = sorted(types)

        if len(sorted_types) == 1:
            return type_mapping.get(sorted_types[0], sorted_types[0])
        elif len(sorted_types) == 2 and "Disruption" in sorted_types and "Hijacking with Misuse" in sorted_types:
            return "Wiper"
        elif len(sorted_types) > 1 and "Ransomware" in sorted_types:
            return "Ransomware"
        elif len(
                sorted_types) == 2 and "Data theft" in sorted_types and "Hijacking with Misuse" in sorted_types or "Hijacking without Misuse" in sorted_types:
            return "Data theft"
        else:
            return list(sorted_types)

    for incident in data:
        incident["incident_type_clean"] = translate_type(incident["incident_type"])

    for incident in data:
        if not isinstance(incident["incident_type_clean"], str):
            if "Data theft & Doxing" in incident["incident_type_clean"]:
                incident["incident_type_clean"] = "Hack and leak"
            elif "Data theft" in incident["incident_type_clean"]:
                incident["incident_type_clean"] = "Data theft"
            else:
                incident["incident_type_clean"] = "Other"
    return data


def clean_initiators(data):
    """Cleans the initiator_name, initiator_country, and initiator_category variables for consistency. Ensure that
    when there is no initiator name, nor country, nor category the code is 'Not attributed'. In cases when one of these
    three variables is known, "Unknown" is assigned to the others."""
    unwanted_values = ["", "Unknown - not attributed", "None", "Not available", "Unknown", None]

    def should_replace_with_unknown(values):
        return all(item in unwanted_values for item in values)

    for incident in data:
        if should_replace_with_unknown(incident["initiator_name"]):
            incident["initiator_name"] = ["Unknown"]
        if should_replace_with_unknown(incident["initiator_country"]):
            incident["initiator_country"] = ["Unknown"]
        if should_replace_with_unknown(incident["initiator_category"]):
            incident["initiator_category"] = ["Unknown"]

        if should_replace_with_unknown(incident["initiator_name"]) and \
           should_replace_with_unknown(incident["initiator_country"]) and \
           should_replace_with_unknown(incident["initiator_category"]):
            incident["initiator_name"] = ["Not attributed"]
            incident["initiator_country"] = ["Not attributed"]
            incident["initiator_category"] = ["Not attributed"]

    return data


def get_clean_data(data, receiver_region=None):
    """Performs all the cleaning steps on the data and returns the cleaned data."""
    data = clean_incidents_dict(data)
    data = clean_receivers(data)
    data = clean_dates(data)
    data = clean_types(data)
    data = replace_empty_strings(data)
    data = clean_initiators(data)
    data = brexit_clean(data, receiver_region=receiver_region)
    return data
