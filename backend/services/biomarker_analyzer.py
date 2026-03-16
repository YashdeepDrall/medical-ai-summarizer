def analyze_biomarkers(data):

    analyzed = []

    for item in data:

        biomarker = item.get("Biomarker")
        value = float(item.get("Value"))
        range_text = item.get("Range")

        status = "Unknown"

        if "-" in range_text:

            low, high = range_text.split("-")

            low = float(low)
            high = float(high)

            if value < low:
                status = "Low"

            elif value > high:
                status = "High"

            else:
                status = "Normal"

        analyzed.append({
            "biomarker": biomarker,
            "value": value,
            "range": range_text,
            "status": status
        })

    return analyzed