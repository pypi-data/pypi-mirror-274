import unittest

from aenum import extend_enum
from superblocks_types.api.v1.service_pb2 import ViewMode as ViewModeProto

from superblocks_agent.enumeration.ViewMode import ViewMode


class TestViewMode(unittest.TestCase):
    def test_items(self):
        self.assertEqual(
            [
                (ViewMode.DEPLOYED, "DEPLOYED"),
                (ViewMode.EDITOR, "EDITOR"),
                (ViewMode.PREVIEW, "PREVIEW"),
            ],
            ViewMode.items(),
        )

    def test_from_str(self):
        self.assertEqual(ViewMode.DEPLOYED, ViewMode.from_str("Deployed"))
        self.assertEqual(ViewMode.EDITOR, ViewMode.from_str("Editor"))
        self.assertEqual(ViewMode.PREVIEW, ViewMode.from_str("Preview"))

        with self.assertRaises(ValueError) as context:
            ViewMode.from_str("invalid")
        self.assertEqual("'invalid' is not a valid ViewMode", str(context.exception))

    def test_to_proto_view_mode(self):
        self.assertEqual(ViewModeProto.VIEW_MODE_DEPLOYED, ViewMode.DEPLOYED.to_proto_view_mode())
        self.assertEqual(ViewModeProto.VIEW_MODE_EDIT, ViewMode.EDITOR.to_proto_view_mode())
        self.assertEqual(ViewModeProto.VIEW_MODE_PREVIEW, ViewMode.PREVIEW.to_proto_view_mode())
        extend_enum(ViewMode, "UNKNOWN", "unknown")
        self.assertEqual(ViewModeProto.VIEW_MODE_UNSPECIFIED, ViewMode.UNKNOWN.to_proto_view_mode())
