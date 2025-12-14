"""
Animation Controller

Generates smooth growth animations by progressively revealing segments.
Supports multiple growth modes: linear, sigmoid, and apical dominance.
"""

import math
import os
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Tuple, Union

# Import 2D segment types
from turtle.interpreter import Segment, BoundingBox

# Try to import 3D segment types
try:
    from turtle.interpreter3d import Segment3D, BoundingBox3D
    HAS_3D = True
except ImportError:
    HAS_3D = False
    Segment3D = None
    BoundingBox3D = None


class GrowthMode(Enum):
    """Growth animation styles."""
    LINEAR = "linear"           # Simple linear reveal
    SIGMOID = "sigmoid"         # S-curve growth (slow-fast-slow)
    APICAL_DOMINANCE = "apical" # Main stem first, branches follow


def ease_out_cubic(t: float) -> float:
    """
    Ease-out cubic function for natural deceleration.
    
    Args:
        t: Input value from 0.0 to 1.0
        
    Returns:
        Eased value from 0.0 to 1.0
    """
    return 1 - (1 - t) ** 3


def ease_out_quad(t: float) -> float:
    """
    Ease-out quadratic function.
    
    Args:
        t: Input value from 0.0 to 1.0
        
    Returns:
        Eased value from 0.0 to 1.0
    """
    return 1 - (1 - t) ** 2


def ease_in_out_cubic(t: float) -> float:
    """
    Ease-in-out cubic function.
    
    Args:
        t: Input value from 0.0 to 1.0
        
    Returns:
        Eased value from 0.0 to 1.0
    """
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - ((-2 * t + 2) ** 3) / 2


def sigmoid_growth(t: float, k: float = 6.0, midpoint: float = 0.5) -> float:
    """
    S-curve growth: slow start, fast middle, slow finish.
    Mimics biological growth patterns.
    
    Args:
        t: Input value from 0.0 to 1.0
        k: Steepness (higher = sharper transition)
        midpoint: Where the inflection point is
        
    Returns:
        Eased value from 0.0 to 1.0
    """
    # Clamp to avoid math overflow
    x = max(-10, min(10, -k * (t - midpoint)))
    raw = 1.0 / (1.0 + math.exp(x))
    # Normalize to ensure 0 maps to 0 and 1 maps to 1
    min_val = 1.0 / (1.0 + math.exp(k * midpoint))
    max_val = 1.0 / (1.0 + math.exp(-k * (1 - midpoint)))
    return (raw - min_val) / (max_val - min_val)


@dataclass
class SegmentGrowthInfo:
    """Growth timing information for a segment."""
    segment_index: int
    birth_time: float      # When this segment starts growing (0.0 to 1.0)
    growth_duration: float # How long it takes to fully grow (fraction of total)
    growth_priority: float # Priority multiplier (1.0 = normal, higher = faster)
    parent_index: Optional[int] = None  # Index of parent segment
    children: List[int] = field(default_factory=list)
    is_terminal: bool = False  # True if this is a leaf/tip segment


class AnimationController:
    """
    Controls smooth growth animation of L-system plants.
    
    Generates POV-Ray scene files for each animation frame with
    progressively growing segments.
    """
    
    def __init__(
        self,
        total_frames: int = 100,
        growth_frames: int = 8,
        stagger_frames: float = 0.5,
        easing_function: Callable[[float], float] = ease_out_cubic,
        growth_mode: GrowthMode = GrowthMode.SIGMOID,
        sigmoid_steepness: float = 8.0,
        apical_delay_per_depth: float = 0.05,
        apical_parent_threshold: float = 0.3,
        enable_secondary_thickening: bool = True,
        thickening_rate: float = 0.05
    ):
        """
        Initialize animation controller.
        
        Args:
            total_frames: Total number of animation frames
            growth_frames: Number of frames for each segment to grow
            stagger_frames: Frame delay between consecutive segment starts
            easing_function: Easing function for smooth animation
            growth_mode: Growth animation style
            sigmoid_steepness: Steepness of sigmoid curve (higher = sharper)
            apical_delay_per_depth: Additional delay per depth level (apical mode)
            apical_parent_threshold: Parent completion % before child starts (apical)
            enable_secondary_thickening: Whether older segments thicken over time
            thickening_rate: Rate of secondary thickening
        """
        self.total_frames = total_frames
        self.growth_frames = growth_frames
        self.stagger_frames = stagger_frames
        self.easing_function = easing_function
        self.growth_mode = growth_mode
        self.sigmoid_steepness = sigmoid_steepness
        self.apical_delay_per_depth = apical_delay_per_depth
        self.apical_parent_threshold = apical_parent_threshold
        self.enable_secondary_thickening = enable_secondary_thickening
        self.thickening_rate = thickening_rate
        
        # Cache for growth info
        self._growth_info_cache: Dict[int, SegmentGrowthInfo] = {}
    
    def _build_segment_hierarchy(self, segments: List[Union[Segment, 'Segment3D']]) -> Dict[int, SegmentGrowthInfo]:
        """
        Build parent-child relationships between segments for apical dominance.
        
        Uses spatial proximity to determine relationships - a segment's parent
        is the previous segment whose end point matches this segment's start.
        """
        growth_info: Dict[int, SegmentGrowthInfo] = {}
        
        # Detect if we're working with 3D segments
        is_3d = HAS_3D and len(segments) > 0 and isinstance(segments[0], Segment3D)
        
        # Initialize all segments
        for i, seg in enumerate(segments):
            growth_info[i] = SegmentGrowthInfo(
                segment_index=i,
                birth_time=0.0,
                growth_duration=self.growth_frames / self.total_frames,
                growth_priority=1.0,
                parent_index=None,
                children=[],
                is_terminal=True  # Assume terminal until proven otherwise
            )
        
        # Build hierarchy based on depth changes and spatial relationships
        tolerance = 0.001
        
        for i, seg in enumerate(segments):
            best_parent = None
            for j in range(i - 1, -1, -1):
                prev_seg = segments[j]
                # Check if previous segment's end matches this segment's start
                if is_3d:
                    if (abs(prev_seg.x2 - seg.x1) < tolerance and 
                        abs(prev_seg.y2 - seg.y1) < tolerance and
                        abs(prev_seg.z2 - seg.z1) < tolerance):
                        best_parent = j
                        break
                else:
                    if (abs(prev_seg.x2 - seg.x1) < tolerance and 
                        abs(prev_seg.y2 - seg.y1) < tolerance):
                        best_parent = j
                        break
            
            if best_parent is not None:
                growth_info[i].parent_index = best_parent
                growth_info[best_parent].children.append(i)
                growth_info[best_parent].is_terminal = False
        
        # Calculate birth times based on apical dominance
        self._calculate_apical_birth_times(segments, growth_info)
        
        return growth_info
    
    def _calculate_apical_birth_times(
        self, 
        segments: List[Segment], 
        growth_info: Dict[int, SegmentGrowthInfo]
    ) -> None:
        """
        Calculate birth times for apical dominance mode.
        
        Main stem grows first, branches start after their parent reaches
        a threshold completion level, with additional delay per depth.
        """
        if not segments:
            return
        
        # Calculate base timing: distribute across available time
        growth_period = 1.0 - (self.growth_frames / self.total_frames)
        if growth_period <= 0:
            growth_period = 0.8
        
        # Process segments in order (BFS from roots)
        processed = set()
        queue = []
        
        # Find root segments (no parent)
        for idx, info in growth_info.items():
            if info.parent_index is None:
                queue.append(idx)
                # Root segments start immediately based on their index
                normalized_idx = idx / len(segments) if len(segments) > 1 else 0
                info.birth_time = normalized_idx * growth_period * 0.3  # First 30% for roots
                info.growth_priority = 1.0
        
        while queue:
            idx = queue.pop(0)
            if idx in processed:
                continue
            processed.add(idx)
            
            info = growth_info[idx]
            seg = segments[idx]
            
            # Calculate priority based on depth
            info.growth_priority = 0.8 ** seg.depth
            
            # Process children
            for child_idx in info.children:
                child_info = growth_info[child_idx]
                child_seg = segments[child_idx]
                
                # Child starts after parent reaches threshold
                parent_completion_time = info.birth_time + info.growth_duration * self.apical_parent_threshold
                depth_delay = child_seg.depth * self.apical_delay_per_depth
                
                child_info.birth_time = min(parent_completion_time + depth_delay, growth_period)
                child_info.growth_priority = 0.8 ** child_seg.depth
                
                queue.append(child_idx)
        
        # Handle any orphan segments (shouldn't happen but be safe)
        for idx in range(len(segments)):
            if idx not in processed:
                normalized_idx = idx / len(segments)
                growth_info[idx].birth_time = normalized_idx * growth_period
    
    def _get_growth_function(self) -> Callable[[float], float]:
        """Get the appropriate growth function for the current mode."""
        if self.growth_mode == GrowthMode.LINEAR:
            return lambda t: t
        elif self.growth_mode == GrowthMode.SIGMOID:
            return lambda t: sigmoid_growth(t, k=self.sigmoid_steepness)
        else:  # APICAL_DOMINANCE uses sigmoid but with modified timing
            return lambda t: sigmoid_growth(t, k=self.sigmoid_steepness)
    
    def calculate_visibility(
        self,
        segment_index: int,
        frame: int,
        num_segments: int
    ) -> float:
        """
        Calculate visibility of a segment at a given frame.
        
        Args:
            segment_index: Index of the segment (0-based)
            frame: Current frame number (0-based)
            num_segments: Total number of segments
            
        Returns:
            Visibility from 0.0 (invisible) to 1.0 (fully visible)
        """
        if num_segments == 0:
            return 0.0
        
        # Get growth function
        growth_func = self._get_growth_function()
        
        # Calculate frame progress (0.0 to 1.0)
        frame_progress = frame / (self.total_frames - 1) if self.total_frames > 1 else 1.0
        
        # Check if we have cached growth info (for apical dominance)
        if segment_index in self._growth_info_cache:
            info = self._growth_info_cache[segment_index]
            
            # Calculate elapsed time since birth
            elapsed = frame_progress - info.birth_time
            
            if elapsed <= 0:
                return 0.0
            
            # Adjust duration by priority
            effective_duration = info.growth_duration / max(info.growth_priority, 0.1)
            
            if elapsed >= effective_duration:
                return 1.0
            
            progress = elapsed / effective_duration
            return growth_func(progress)
        
        # Fallback: simple timing based on index
        growth_period = 1.0 - (self.growth_frames / self.total_frames)
        if growth_period <= 0:
            growth_period = 0.8
        
        start_time = (segment_index / num_segments) * growth_period
        growth_duration = self.growth_frames / self.total_frames
        
        elapsed = frame_progress - start_time
        
        if elapsed <= 0:
            return 0.0
        elif elapsed >= growth_duration:
            return 1.0
        else:
            progress = elapsed / growth_duration
            return growth_func(progress)
    
    def calculate_thickness_multiplier(
        self,
        segment_index: int,
        frame: int,
        num_segments: int
    ) -> float:
        """
        Calculate thickness multiplier for secondary thickening effect.
        
        Older segments (those that started growing earlier) gradually thicken.
        Implements a simplified pipe model effect.
        
        Args:
            segment_index: Index of the segment
            frame: Current frame number
            num_segments: Total number of segments
            
        Returns:
            Thickness multiplier (1.0 = no change, >1.0 = thicker)
        """
        if not self.enable_secondary_thickening:
            return 1.0
        
        frame_progress = frame / (self.total_frames - 1) if self.total_frames > 1 else 1.0
        
        # Get birth time
        if segment_index in self._growth_info_cache:
            birth_time = self._growth_info_cache[segment_index].birth_time
        else:
            growth_period = 1.0 - (self.growth_frames / self.total_frames)
            birth_time = (segment_index / num_segments) * growth_period
        
        # Calculate age (how long since fully grown)
        visibility = self.calculate_visibility(segment_index, frame, num_segments)
        if visibility < 1.0:
            return 1.0  # Not fully grown yet
        
        # Age is time since becoming fully visible
        growth_duration = self.growth_frames / self.total_frames
        fully_grown_time = birth_time + growth_duration
        age = max(0, frame_progress - fully_grown_time)
        
        # Logarithmic thickening: radius *= 1 + rate * log(1 + age)
        return 1.0 + self.thickening_rate * math.log(1 + age * 10)
    
    def get_frame_segments(
        self,
        all_segments: List[Union[Segment, 'Segment3D']],
        frame: int
    ) -> List[Union[Segment, 'Segment3D']]:
        """
        Get segments with visibility applied for a specific frame.
        
        Args:
            all_segments: Complete list of segments (2D or 3D)
            frame: Current frame number
            
        Returns:
            List of segments with partial visibility applied
        """
        num_segments = len(all_segments)
        visible_segments = []
        
        # Detect if we're working with 3D segments
        is_3d = HAS_3D and len(all_segments) > 0 and isinstance(all_segments[0], Segment3D)
        
        for i, segment in enumerate(all_segments):
            visibility = self.calculate_visibility(i, frame, num_segments)
            
            if visibility > 0.001:  # Only include visible segments
                partial = segment.partial(visibility)
                
                # Apply secondary thickening
                if self.enable_secondary_thickening:
                    thickness_mult = self.calculate_thickness_multiplier(i, frame, num_segments)
                    
                    if is_3d:
                        partial = Segment3D(
                            x1=partial.x1, y1=partial.y1, z1=partial.z1,
                            x2=partial.x2, y2=partial.y2, z2=partial.z2,
                            depth=partial.depth,
                            width=partial.width * thickness_mult,
                            index=partial.index,
                            heading=partial.heading
                        )
                    else:
                        partial = Segment(
                            x1=partial.x1,
                            y1=partial.y1,
                            x2=partial.x2,
                            y2=partial.y2,
                            depth=partial.depth,
                            width=partial.width * thickness_mult,
                            index=partial.index
                        )
                
                # Only include if segment has some length
                if partial.length() > 0.001:
                    visible_segments.append(partial)
        
        return visible_segments
    
    def get_terminal_segments(self, all_segments: List[Segment]) -> List[int]:
        """
        Get indices of terminal (leaf) segments.
        
        Terminal segments are those that have no children - they're at branch tips.
        """
        if self._growth_info_cache:
            return [idx for idx, info in self._growth_info_cache.items() if info.is_terminal]
        
        # Fallback: segments at max depth or with specific characteristics
        if not all_segments:
            return []
        
        max_depth = max(seg.depth for seg in all_segments)
        return [i for i, seg in enumerate(all_segments) if seg.depth == max_depth]
    
    def prepare_segments(self, segments: List[Union[Segment, 'Segment3D']]) -> None:
        """
        Prepare segment hierarchy and growth info before animation.
        
        Call this before generate_frames() to set up apical dominance.
        """
        if self.growth_mode == GrowthMode.APICAL_DOMINANCE:
            self._growth_info_cache = self._build_segment_hierarchy(segments)
        else:
            self._growth_info_cache = {}
    
    def generate_frames(
        self,
        segments: List[Union[Segment, 'Segment3D']],
        bbox: Union[BoundingBox, 'BoundingBox3D'],
        generator,  # POVRayGenerator - avoid circular import
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[str]:
        """
        Generate all animation frame .pov files.
        
        Args:
            segments: Complete list of segments (2D or 3D)
            bbox: Bounding box for camera (use full plant bbox)
            generator: POVRayGenerator instance
            progress_callback: Optional callback(current_frame, total_frames)
            
        Returns:
            List of paths to generated .pov files
        """
        # Prepare segment hierarchy for apical dominance
        self.prepare_segments(segments)
        
        pov_files = []
        max_depth = max((seg.depth for seg in segments), default=0)
        terminal_indices = set(self.get_terminal_segments(segments))
        
        for frame in range(self.total_frames):
            # Get segments visible at this frame
            frame_segments = self.get_frame_segments(segments, frame)
            
            # Mark terminal segments for leaf rendering
            frame_terminal = []
            for seg in frame_segments:
                if seg.index in terminal_indices:
                    frame_terminal.append(seg)
            
            # Generate POV-Ray scene
            pov_file = generator.generate_frame(
                frame_segments,
                bbox,
                frame,
                max_depth,
                terminal_segments=frame_terminal
            )
            pov_files.append(pov_file)
            
            if progress_callback:
                progress_callback(frame + 1, self.total_frames)
        
        return pov_files
    
    def auto_configure(self, num_segments: int, respect_total_frames: bool = True) -> int:
        """
        Auto-configure animation parameters based on segment count.
        
        Args:
            num_segments: Number of segments in the plant
            respect_total_frames: If True, don't increase total_frames
            
        Returns:
            Suggested minimum frames (for information only)
        """
        # Adjust growth frames based on total segments
        if num_segments < 50:
            self.growth_frames = 12
        elif num_segments < 200:
            self.growth_frames = 8
        elif num_segments < 500:
            self.growth_frames = 6
        else:
            self.growth_frames = 4
        
        # Calculate suggested minimum frames
        min_frames = int(num_segments * 0.1 + self.growth_frames * 2)
        
        if not respect_total_frames and self.total_frames < min_frames:
            self.total_frames = min_frames
        
        return min_frames


class GrowthPreview:
    """Preview growth animation data without rendering."""
    
    @staticmethod
    def generate_preview_data(
        segments: List[Segment],
        controller: AnimationController,
        sample_frames: int = 10
    ) -> List[dict]:
        """
        Generate preview data for animation frames.
        
        Args:
            segments: Complete list of segments
            controller: AnimationController instance
            sample_frames: Number of sample frames to generate
            
        Returns:
            List of dicts with frame statistics
        """
        controller.prepare_segments(segments)
        num_segments = len(segments)
        previews = []
        
        frame_step = max(1, controller.total_frames // sample_frames)
        
        for frame in range(0, controller.total_frames, frame_step):
            visible_count = 0
            total_visibility = 0.0
            
            for i, seg in enumerate(segments):
                vis = controller.calculate_visibility(i, frame, num_segments)
                if vis > 0:
                    visible_count += 1
                    total_visibility += vis
            
            previews.append({
                'frame': frame,
                'visible_segments': visible_count,
                'total_segments': num_segments,
                'average_visibility': total_visibility / num_segments if num_segments > 0 else 0,
                'percent_complete': visible_count / num_segments * 100 if num_segments > 0 else 0
            })
        
        return previews
