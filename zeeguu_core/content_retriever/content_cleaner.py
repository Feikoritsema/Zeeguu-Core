import zeeguu_core


def cleanup_non_content_bits(text: str):
    """

        Sometimes newspaper still leaves some individual fragments
        in the article.text.


    :param text:
    :return:
    """
    new_text = text

    new_text = new_text.replace("\nAdvertisement\n", "")

    new_text = new_text.replace("\ntrue\n", "")
    if new_text != text:
        zeeguu_core.log("clean")

    return new_text
