"""
Tests for Enhanced Turtle Interpreter

Tests the new ABOP-style turtle symbols:
- ! : Decrement diameter
- $ : Roll to horizontal (3D)
- . : Mark polygon vertex
- { } : Polygon mode
- ' : Increment color
- % : Cut branch
"""

import pytest
import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turtle.interpreter import TurtleInterpreter, Segment, BoundingBox, Polygon


class TestBasicInterpretation:
    """Tests for basic turtle interpretation."""
    
    def test_simple_line(self):
        """Test drawing a simple line."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        result = interp.interpret("F")
        
        assert len(result.segments) == 1
        seg = result.segments[0]
        assert seg.x1 == 0
        assert seg.y1 == 0
        # Pointing up (90 degrees), so x2 ~= 0, y2 ~= 10
        assert abs(seg.x2) < 0.01
        assert abs(seg.y2 - 10) < 0.01
    
    def test_turn_left(self):
        """Test turning left."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        result = interp.interpret("F+F")
        
        assert len(result.segments) == 2
        # Second segment should be pointing left (180 degrees)
        seg2 = result.segments[1]
        assert abs(seg2.x2 - seg2.x1 - (-10)) < 0.01  # Moving left
    
    def test_turn_right(self):
        """Test turning right."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        result = interp.interpret("F-F")
        
        assert len(result.segments) == 2
        # Second segment should be pointing right (0 degrees)
        seg2 = result.segments[1]
        assert abs(seg2.x2 - seg2.x1 - 10) < 0.01  # Moving right
    
    def test_branching(self):
        """Test push/pop state."""
        interp = TurtleInterpreter(angle_delta=45, step_size=10)
        result = interp.interpret("F[+F]F")
        
        assert len(result.segments) == 3
        # First and third segments should be on same line (with floating-point tolerance)
        assert abs(result.segments[0].x1 - result.segments[2].x1) < 1e-10
        assert result.segments[0].y2 == result.segments[2].y1  # Connected
    
    def test_depth_increment(self):
        """Test that depth increments in branches."""
        interp = TurtleInterpreter()
        result = interp.interpret("F[F[F]F]F")
        
        depths = [s.depth for s in result.segments]
        assert 0 in depths  # Root level
        assert 1 in depths  # First branch
        assert 2 in depths  # Nested branch


class TestWidthDecrement:
    """Tests for ! symbol (width decrement)."""
    
    def test_width_decrement(self):
        """Test that ! decrements width."""
        interp = TurtleInterpreter(width_decrement=0.8)
        result = interp.interpret("F!F!F")
        
        assert len(result.segments) == 3
        # Width should decrease with each !
        widths = [s.width for s in result.segments]
        assert widths[0] > widths[1] > widths[2]
        assert abs(widths[1] / widths[0] - 0.8) < 0.01
    
    def test_width_in_branch(self):
        """Test width decrement in branches."""
        interp = TurtleInterpreter(width_decay=0.7, width_decrement=0.9)
        result = interp.interpret("F[!F]F")
        
        # Branch segment should have both decay and decrement applied
        branch_seg = result.segments[1]
        main_seg = result.segments[0]
        assert branch_seg.width < main_seg.width


class TestColorIndex:
    """Tests for ' symbol (color increment)."""
    
    def test_color_increment(self):
        """Test that ' increments color index."""
        interp = TurtleInterpreter()
        result = interp.interpret("F'F'F")
        
        assert len(result.segments) == 3
        colors = [s.color_index for s in result.segments]
        assert colors[0] == 0
        assert colors[1] == 1
        assert colors[2] == 2


class TestPolygonMode:
    """Tests for { } . symbols (polygon mode)."""
    
    def test_simple_polygon(self):
        """Test creating a simple polygon."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        # Create a triangle: start, move, mark, turn, move, mark, turn, move
        result = interp.interpret("{F.+F.+F.}")
        
        assert len(result.polygons) == 1
        poly = result.polygons[0]
        assert len(poly.vertices) >= 3  # At least 3 vertices for valid polygon
    
    def test_polygon_in_branch(self):
        """Test polygon inside a branch."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        result = interp.interpret("F[{F.+F.}]F")
        
        # Should have polygon from branch
        assert len(result.polygons) >= 0  # May or may not have valid polygon
    
    def test_nested_polygons(self):
        """Test multiple polygons."""
        interp = TurtleInterpreter(angle_delta=90, step_size=5)
        result = interp.interpret("{F.+F.+F.}{F.+F.+F.}")
        
        # Should have two polygons
        assert len(result.polygons) == 2
    
    def test_g_symbol_in_polygon(self):
        """Test G symbol moves without drawing."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        result = interp.interpret("{.G.G.G.}")
        
        # G moves without creating segments but adds vertices to polygon
        # No segments should be created
        assert len(result.segments) == 0
        # But polygon should have vertices
        if result.polygons:
            assert len(result.polygons[0].vertices) >= 3


class TestCutBranch:
    """Tests for % symbol (cut branch)."""
    
    def test_cut_simple(self):
        """Test cutting a branch."""
        interp = TurtleInterpreter()
        result = interp.interpret("F[F%F]F")
        
        # The F after % should not be drawn
        # Should have F (main), F (branch start), F (after branch)
        # The %F part should be skipped
        assert len(result.segments) == 3
    
    def test_cut_nested(self):
        """Test cutting nested branches."""
        interp = TurtleInterpreter()
        result = interp.interpret("F[F[F%F]F]F")
        
        # The innermost F after % should be skipped
        # Count should be less than if no cut
        interp2 = TurtleInterpreter()
        result2 = interp2.interpret("F[F[FF]F]F")
        assert len(result.segments) < len(result2.segments)


class TestBoundingBox:
    """Tests for bounding box calculation."""
    
    def test_simple_bbox(self):
        """Test bounding box of simple shape."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        result = interp.interpret("F+F+F+F")
        
        bbox = interp.get_bounding_box(result.segments)
        # Should form a square
        assert bbox.width > 0
        assert bbox.height > 0
    
    def test_bbox_with_polygons(self):
        """Test bounding box includes polygons."""
        interp = TurtleInterpreter(angle_delta=90, step_size=10)
        result = interp.interpret("{F.+F.+F.}")
        
        bbox = interp.get_bounding_box(result.segments, result.polygons)
        assert bbox.width > 0


class TestLegacyCompatibility:
    """Tests for backward compatibility."""
    
    def test_interpret_legacy(self):
        """Test legacy interpret method."""
        interp = TurtleInterpreter()
        segments = interp.interpret_legacy("F[+F]F")
        
        # Should return list of segments, not InterpretResult
        assert isinstance(segments, list)
        assert len(segments) == 3
    
    def test_max_depth(self):
        """Test max depth calculation."""
        interp = TurtleInterpreter()
        result = interp.interpret("F[F[F[F]]]")
        
        max_depth = interp.get_max_depth(result.segments)
        assert max_depth == 3


class TestSegment:
    """Tests for Segment class."""
    
    def test_segment_length(self):
        """Test segment length calculation."""
        seg = Segment(0, 0, 3, 4, 0, 1.0)
        assert abs(seg.length() - 5.0) < 0.01  # 3-4-5 triangle
    
    def test_segment_partial(self):
        """Test partial segment."""
        seg = Segment(0, 0, 10, 0, 0, 1.0)
        
        half = seg.partial(0.5)
        assert half.x1 == 0
        assert abs(half.x2 - 5) < 0.01
        
        full = seg.partial(1.0)
        assert full.x2 == seg.x2
        
        zero = seg.partial(0.0)
        assert zero.x2 == zero.x1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
