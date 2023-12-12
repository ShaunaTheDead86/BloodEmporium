import math


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def xy(self):
        return self.x, self.y

    def scale(self, ratio):
        self.x *= ratio
        self.y *= ratio

    def distance_pos(self, other):
        return math.pow((self.x - other.x) ** 2 + (self.y - other.y) ** 2, 0.5)

    def distance_xy(self, x, y):
        return math.pow((self.x - x) ** 2 + (self.y - y) ** 2, 0.5)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other


class Box:
    def __init__(self, x1, y1, x2, y2):
        self.nw = Position(x1, y1)
        self.se = Position(x2, y2)

    def scale(self, ratio):
        self.nw.scale(ratio)
        self.se.scale(ratio)

    def xyxy(self):
        return self.nw.x, self.nw.y, self.se.x, self.se.y

    def centre(self) -> Position:
        return Position((self.nw.x + self.se.x) // 2, (self.nw.y + self.se.y) // 2)

    def dimensions(self):  # width, height
        return abs(self.nw.x - self.se.x), abs(self.nw.y - self.se.y)

    def diameter(self):
        return (abs(self.nw.x - self.se.x) + abs(self.nw.y - self.se.y)) / 2

    def close_to(self, other):
        return self.centre().distance_pos(other.centre()) < max(
            self.diameter(), other.diameter()
        )

    def close_to_xy(self, x, y):
        return self.centre().distance_xy(x, y) < self.diameter()

    def intersects(self, other):
        # separating axis theorem
        return not (
            self.se.x < other.nw.x
            or self.nw.x > other.se.x
            or self.se.y < other.nw.y
            or self.nw.y > other.se.y
        )

    def __eq__(self, other):
        return self.nw == other.nw and self.se == other.se

    def __ne__(self, other):
        return not self == other


class UnmatchedNode:
    def __init__(self, box: Box, confidence, cls_name):
        self.box = box
        self.confidence = confidence
        self.cls_name = cls_name

    def xyxy(self):
        return self.box.xyxy()

    def __eq__(self, other):
        return self.box == other.box

    def __ne__(self, other):
        return not self == other


class MatchedNode(UnmatchedNode):
    def __init__(self, box: Box, confidence, cls_name, unique_id=""):
        super().__init__(box, confidence, cls_name)
        self.unique_id = unique_id  # same as unlockable unique id

    @staticmethod
    def from_unmatched_node(unmatched_node: UnmatchedNode, unique_id=""):
        return MatchedNode(
            unmatched_node.box,
            unmatched_node.confidence,
            unmatched_node.cls_name,
            unique_id,
        )
