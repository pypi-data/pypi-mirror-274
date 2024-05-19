from csv import DictReader
from lxml import etree
from lxml.builder import ElementMaker
from datetime import datetime
import uuid


class XMLGenerator:
    def __init__(self, csv_file, email, name):
        self.csv_file = csv_file
        self.email = email
        self.name = name
        self.csv_contents = self.__read_csv()
        self.xml = self.construct_xml()

    def __read_csv(self):
        with open(self.csv_file, "r") as file:
            reader = DictReader(file)
            return [row for row in reader]

    def construct_xml(self):
        head = Head(self.email, self.name)
        body = Body(self.csv_contents)
        xml = CrossrefXML(head.head_xml, body.body_xml)
        return xml.xml

    def write_xml(self, output_file):
        with open(output_file, "wb") as file:
            file.write(
                etree.tostring(
                    self.xml, pretty_print=True, xml_declaration=True, encoding="UTF-8"
                )
            )


class CrossrefElement:
    def __init__(self):
        self.cr = self.__build_namespace("http://www.crossref.org/schema/5.3.1", None)
        self.xsi = self.__build_namespace(
            "http://www.w3.org/2001/XMLSchema-instance", "xsi"
        )

    @staticmethod
    def __build_namespace(uri, short):
        return ElementMaker(
            namespace=uri,
            nsmap={
                short: uri,
            },
        )


class Head(CrossrefElement):
    def __init__(
        self,
        email,
        name,
    ):
        super().__init__()
        self.email = email
        self.name = name
        self.head_xml = self.create()

    def create(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return self.cr.head(
            self.cr.doi_batch_id(f"UTIA_{timestamp}"),
            self.cr.timestamp(timestamp),
            self.cr.depositor(
                self.cr.depositor_name(self.name), self.cr.email_address(self.email)
            ),
            self.cr.registrant(
                "University of Tennessee Extension - Institute of Agriculture"
            ),
        )


class Title(CrossrefElement):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.title_xml = self.__create_title()

    def create(self):
        return self.cr.titles(self.cr.title(self.title))


class Body(CrossrefElement):
    def __init__(self, reports):
        super().__init__()
        self.reports = reports
        self.body_xml = self.create()

    def create(self):
        return self.cr.body(*self.add_reports())

    def add_reports(self):
        all_reports = []
        for report in self.reports:
            report_xml = ReportPaper(report)
            all_reports.append(report_xml.report_xml)
        return all_reports


class CrossrefXML(CrossrefElement):
    def __init__(self, head, body):
        super().__init__()
        self.head = head
        self.body = body
        self.xml = self.create()

    def create(self):
        begin = self.cr.doi_batch(self.head, self.body)
        begin.attrib["{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"] = (
            "http://www.crossref.org/schema/5.3.1 http://www.crossref.org/schemas/crossref5.3.1.xsd"
        )
        begin.attrib["version"] = "5.3.1"
        return begin


class ReportPaper(CrossrefElement):
    def __init__(self, report_metadata):
        super().__init__()
        self.report = report_metadata
        self.report_xml = self.create()

    def create(self):
        if self.report["Expires"] == "N":
            return self.cr.__call__(
                "report-paper",
                DOIData(
                    resource=self.report["URL to Landing Page"],
                    expires=self.report["Expires"],
                ).doi_data,
                self.cr.titles(self.cr.title(self.report["Title"])),
                self.cr.publisher_item(self.add_item_number(self.report["PubNumber"])),
                self.cr.publication_date(
                    PublicationDate(self.report["DatePublished"]).date_xml
                ),
                self.cr.contributors(
                    ContributorList(self.report["AuthorList"]).contributor_xml
                ),
                Institution().institution_xml,
            )
        else:
            return self.cr.__call__(
                "report-paper", ReportPaperSeries(self.report).report_xml
            )

    def add_item_number(self, pub_number):
        number = self.cr.item_number(pub_number)
        number.attrib["item_number_type"] = "Report Number"
        return number


class PublicationDate(CrossrefElement):
    def __init__(self, date):
        super().__init__()
        self.date = date
        self.month = date.split("/")[0]
        self.day = date.split("/")[1]
        self.year = date.split("/")[2]
        self.date_xml = self.create()

    def create(self):
        return self.cr.publication_date(
            self.cr.month(self.month), self.cr.day(self.day), self.cr.year(self.year)
        )


class ContributorList(CrossrefElement):
    def __init__(self, contributors):
        super().__init__()
        self.contributors = contributors.split(" | ")
        self.contributor_xml = self.create()

    def create(self):
        return self.cr.contributors(*self.add_contributors())

    def add_contributors(self):
        all_contributors = []
        for contributor in self.contributors:
            surname = contributor.split(",")[0].strip()
            given_name = contributor.split(",")[1].strip()
            contributor_xml = self.cr.person_name(
                self.cr.surname(surname), self.cr.given_name(given_name)
            )
            all_contributors.append(contributor_xml)
        return all_contributors


class Institution(CrossrefElement):
    def __init__(self):
        super().__init__()
        self.institution_xml = self.create()

    def create(self):
        return self.cr.institution(
            self.cr.institution_name("University of Tennessee Extension"),
            self.cr.institution_id(self.build_identifier()),
        )

    def build_identifier(self):
        institution_id = self.cr.institution_id("0000 0000 9091 7939")
        institution_id.attrib["value"] = "isni"
        return institution_id


class DOIData(CrossrefElement):
    def __init__(self, resource, expires, type="Report"):
        super().__init__()
        self.resource = resource
        self.expires = expires
        self.type = type
        self.doi_data = self.create()

    def create(self):
        if self.expires == "N" or self.type == "Series":
            return self.cr.doi_data(
                self.cr.doi(f"10.7290/UTIA-{uuid.uuid4()}"),
                self.cr.resource(self.resource),
            )
        else:
            return self.cr.doi_data()


class ReportPaperSeries(CrossrefElement):
    def __init__(self, report_metadata):
        super().__init__()
        self.report = report_metadata
        self.report_xml = self.create()

    def create(self):
        return self.cr.__call__(
            "report-paper_series_metadata",
            self.cr.series_metadata(
                self.cr.titles(self.cr.title(self.report["Title"])),
                self.cr.publisher_item(self.add_item_number(self.report["PubNumber"])),
                self.cr.publication_date(
                    PublicationDate(self.report["DatePublished"]).date_xml
                ),
                self.cr.contributors(
                    ContributorList(self.report["AuthorList"]).contributor_xml
                ),
                Institution().institution_xml,
            ),
            DOIData(
                resource=self.report["URL to Landing Page"],
                expires=self.report["Expires"],
                type="Series",
            ).doi_data,
            self.cr.titles(self.cr.title(self.report["ParentSeries"])),
        )

    def add_item_number(self, pub_number):
        number = self.cr.item_number(pub_number)
        number.attrib["item_number_type"] = "Report Number"
        return number
