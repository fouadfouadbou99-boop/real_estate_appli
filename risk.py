def risk_score(

        vacancy,

        ltv,

        debt_rate,

        tenant_concentration=0.50):

    score = (

            vacancy * 20 +

            ltv * 30 +

            debt_rate * 20 +

            tenant_concentration * 30
    )

    return round(score, 2)


def risk_category(score):

    if score < 30:
        return "Faible"

    elif score < 60:
        return "Moyen"

    else:
        return "Elevé"
