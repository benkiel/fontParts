import weakref
from fontParts.base.errors import FontPartsError
from fontParts.base.base import BaseObject, dynamicProperty
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedFeatures


class BaseFeatures(BaseObject, DeprecatedFeatures):

    copyAttributes = ("text",)

    def _reprContents(self):
        contents = []
        if self.font is not None:
            contents.append("for font")
            contents += self.font._reprContents()
        return contents

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        Return the features' parent :class:`BaseFont`.
        This is a backwards compatibility method.
        """
        return self.font

    # Font

    _font = None

    font = dynamicProperty("font", "The features' parent :class:`BaseFont`.")

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        assert self._font is None or self._font() == font
        if font is not None:
            font = weakref.ref(font)
        self._font = font

    # ----
    # Text
    # ----

    text = dynamicProperty(
        "base_text",
        """
        The `.fea formated <http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html>`_
        text representing the features.
        It must be a :ref:`type-string`.
        """
    )

    def _get_base_text(self):
        value = self._get_text()
        if value is not None:
            value = normalizers.normalizeFeatureText(value)
        return value

    def _set_base_text(self, value):
        if value is not None:
            value = normalizers.normalizeFeatureText(value)
        self._set_text(value)

    def _get_text(self):
        """
        This is the environment implementation of
        :attr:`BaseFeatures.text`. This must return a
        :ref:`type-string`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_text(self, value):
        """
        This is the environment implementation of
        :attr:`BaseFeatures.text`. **value** will be
        a :ref:`type-string`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()
