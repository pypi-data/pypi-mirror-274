import numpy as np


def brightness(image, val):
    """Adjust image brightness.

    :param image: Input image.
    :param val: Brightness adjustment factor in units of the image's
           dynamic range (+/-).
    :return: Brightness-adjusted image.
    """
    return image + val


def contrast(image, val: float):
    """Adjust image contrast.

    Note that this is a simple contrast adjustment that corresponds to the
    Legacy method in Photoshop.

    :param image: Input image.
    :param val: Contrast adjustment factor (+/-). Positive values increase
           contrast while negative values decrease contrast. Values below -1
           will invert the image.
    :return: Contrast-adjusted image.
    """
    val = val + 1.
    return val * image + 0.5 * (1. - val)


def brightness_contrast(image: np.ndarray, b: float, c):
    """Apply a brightness-contrast adjustment.

    :param image: Input image.
    :param b: Brightness adjustment factor in units of the image's dynamic
           range (+/-).
    :param c: Contrast adjustment factor (+/-). Positives values increase
           contrast while negative values decrease contrast.
    :return: Brightness/contrast-adjusted image.
    """
    return contrast(brightness(image, b), c)


def exposure(image, val):
    """Increase image exposure.

    :param image: Input image.
    :param val: Exposure adjustment factor (+/-).
    :return: Exposure-adjusted image.
    """
    return image * 2 ** val


def shadows(image, val):
    """Image shadow adjustment.

    Adapted from an implementation by
    `HViktorTsoi <https://gist.github.com/HViktorTsoi/8e8b0468a9fb07842669aa368382a7df>`_.

    :param image: Input image.
    :param val: Shadow adjustment factor (+/-).
    :return: Exposure-adjusted image.
    """
    shadow_val = 1. + val / 100. * 2
    shadow_mid = 3. / 10.
    shadow_region = np.clip(1. - image / shadow_mid, 0, 1)
    shadow_region[np.where(image >= shadow_mid)] = 0
    return (1 - shadow_region) * image + shadow_region * (
            1 - np.power(1 - image, shadow_val))
