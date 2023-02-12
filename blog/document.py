from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class PostDocument(DocType):
    title = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    date_posted = Date()

    class Meta:
        index = "posts"
