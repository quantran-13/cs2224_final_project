_label_content_start = """
<div class="col-6 align-self-center">
    <div class="border-0">
        <ul class="list-group list-group-flush">
"""


_label_content_li_start = """
<li class="list-group-item">
    <div class="d-flex flex-row justify-content-start align-items-center">
        <div class="flex-shrink-0">
            <img class="align-self-center" style="max-width: 100px; height: auto;" src="data:image/png;base64, {}" />
        </div>
        <div class="flex-grow-1 ms-3">
            <ul class="list-unstyled">
                <ul>
"""


_label_content_li_nested = """
<li>{} - {:.2f}</li>
"""


_label_content_li_end = """
                </ul>
            </ul>
        </div>
    </div>
</li>
"""


_label_content_end = """
        </ul>
    </div>
</div>
"""
