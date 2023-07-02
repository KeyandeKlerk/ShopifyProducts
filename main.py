import csv
import requests
import xml.etree.ElementTree as ET


def parse_xml_to_csv(xml_string):
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Open a CSV file for writing with UTF-8 encoding
    with open("products.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)

        # Write the CSV header
        writer.writerow(
            [
                "Handle",
                "Title",
                "Option1 Name",
                "Option1 Value",
                "Option2 Name",
                "Option2 Value",
                "Option3 Name",
                "Option3 Value",
                "SKU",
                "HS Code",
                "COO",
                "Location",
                "Incoming",
                "Unavailable",
                "Committed",
                "Available",
                "On Hand",
            ]
        )

        # Iterate over each <Product> element
        for product_elem in root.findall("Product"):
            # Extract the data for each field
            name = product_elem.findtext("name").strip().replace(",", "&")
            handle = name.replace(" ", "-").replace("---", "-")
            quantity = product_elem.findtext("quantity")
            sku = product_elem.findtext("sku")
            if int(quantity) > 0:
                # Write the row to the CSV file
                writer.writerow(
                    [
                        handle,
                        name,
                        "Title",
                        "Default Title",
                        "",
                        "",
                        "",
                        "",
                        sku,
                        "",
                        "",
                        "4aKid & 4aPet",
                        "0",
                        "0",
                        "0",
                        quantity,
                        quantity,
                    ]
                )

    print("Conversion completed successfully. CSV file created: 'products.csv'")


def send_request_and_convert_to_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        xml_data = response.content.decode("utf-8")
        parse_xml_to_csv(xml_data)
    else:
        print(
            f"Failed to retrieve XML data from {url}. Status code:",
            response.status_code,
        )


def main():
    # Read URLs from the "url.txt" file
    with open("url.txt", "r") as file:
        urls = file.read().splitlines()

    # Iterate over each URL and send a request for each one
    for url in urls:
        send_request_and_convert_to_csv(url)


if __name__ == "__main__":
    main()
