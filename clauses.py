"""Clause libraries: each builder returns (title, [(heading, text), ...])."""


def rental(d):
    return "RENTAL AGREEMENT", [
        ("Parties", f"This agreement is made at {d['place']} between {d['name']} (the Tenant) and {d['other_party']} (the Landlord)."),
        ("Premises", f"The Landlord lets the premises described as: {d['purpose']}."),
        ("Term", f"The tenancy is for {d['duration']} from the date of signing."),
        ("Rent", f"The Tenant shall pay monthly rent of Rs. {d['amount']} on or before the 5th of every month."),
        ("Security Deposit", f"The Tenant has paid an interest-free refundable deposit of Rs. {d['deposit']}, returnable on vacating after adjusting lawful dues."),
        ("Maintenance", "The Tenant shall keep the premises in good condition. Structural repairs are the Landlord's responsibility."),
        ("Termination", f"Either party may terminate this agreement by giving {d['notice']} written notice."),
        ("Legal Compliance", "The parties shall comply with applicable law, including local stamp-duty and registration requirements."),
    ]


def nda(d):
    return "NON-DISCLOSURE AGREEMENT", [
        ("Parties", f"This agreement is made at {d['place']} between {d['name']} (the Receiving Party) and {d['other_party']} (the Disclosing Party)."),
        ("Confidential Information", f"Confidential Information means all non-public information relating to: {d['purpose']}."),
        ("Obligations", "The Receiving Party shall use the information only for the stated purpose and protect it with reasonable care."),
        ("Exclusions", "Information that is public, already known, or independently developed is not confidential."),
        ("Term", f"The confidentiality obligations continue for {d['duration']}."),
        ("Remedies", "The parties acknowledge that breach may cause harm and that the Disclosing Party may seek appropriate legal remedies."),
        ("Return of Material", f"On request, or within {d['notice']} of termination, all confidential material shall be returned or destroyed."),
    ]


def employment(d):
    return "EMPLOYMENT AGREEMENT", [
        ("Parties", f"This agreement is made at {d['place']} between {d['name']} (the Employee) and {d['other_party']} (the Employer)."),
        ("Position", f"The Employee is appointed for the role of: {d['purpose']}."),
        ("Term", f"The employment period is {d['duration']}, subject to a probation review."),
        ("Remuneration", f"The Employer shall pay a monthly salary of Rs. {d['amount']}, subject to statutory deductions."),
        ("Duties", "The Employee shall perform assigned duties diligently and follow company policies."),
        ("Confidentiality", "The Employee shall not disclose confidential business information during or after employment."),
        ("Termination", f"Either party may end this agreement with {d['notice']} written notice."),
    ]


def leave(d):
    return "LEAVE AND LICENSE AGREEMENT", [
        ("Parties", f"This agreement is made at {d['place']} between {d['name']} (the Licensee) and {d['other_party']} (the Licensor)."),
        ("Licensed Premises", f"The Licensor grants a licence to use: {d['purpose']}."),
        ("Licence Period", f"The licence period is {d['duration']}."),
        ("Licence Fee", f"The Licensee shall pay a monthly licence fee of Rs. {d['amount']}."),
        ("Security Deposit", f"A refundable deposit of Rs. {d['deposit']} has been paid to the Licensor."),
        ("Nature of Licence", "This is a personal licence and does not create any tenancy or interest in the property."),
        ("Termination", f"Either party may terminate this licence with {d['notice']} written notice."),
        ("Registration", "The parties shall complete registration and stamp-duty formalities as required by local law."),
    ]


BUILDERS = {"rental": rental, "nda": nda, "employment": employment, "leave": leave}


def generate_document(doc_type, data):
    return BUILDERS[doc_type](data)
