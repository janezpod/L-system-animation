"""
Animation Controller

Generates smooth growth animations by progressively revealing segments.
"""

import os
from typing import List, Optional, Callable
from turtle.interpreter import Segment, BoundingBox, TurtleInterpreter
from povray.generator import POVRayGenerator


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
        easing_function: Callable[[float], float] = ease_out_cubic
    ):
        """
        Initialize animation controller.
        
        Args:
            total_frames: Total number of animation frames
            growth_frames: Number of frames for each segment to grow
            stagger_frames: Frame delay between consecutive segment starts
            easing_function: Easing function for smooth animation
        """
        self.total_frames = total_frames
        self.growth_frames = growth_frames
        self.stagger_frames = stagger_frames
        self.easing_function = easing_function
    
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
        
        # Calculate when this segment starts growing
        # Distribute start times across available frames
        growth_period = self.total_frames - self.growth_frames
        if growth_period <= 0:
            growth_period = self.total_frames * 0.8
        
        # Start time for this segment
        start_frame = (segment_index / num_segments) * growth_period
        
        # Calculate progress for this segment
        elapsed = frame - start_frame
        
        if elapsed <= 0:
            return 0.0
        elif elapsed >= self.growth_frames:
            return 1.0
        else:
            # Apply easing function
            progress = elapsed / self.growth_frames
            return self.easing_function(progress)
    
    def get_frame_segments(
        self,
        all_segments: List[Segment],
        frame: int
    ) -> List[Segment]:
        """
        Get segments with visibility applied for a specific frame.
        
        Args:
            all_segments: Complete list of segments
            frame: Current frame number
            
        Returns:
            List of segments with partial visibility applied
        """
        num_segments = len(all_segments)
        visible_segments = []
        
        for i, segment in enumerate(all_segments):
            visibility = self.calculate_visibility(i, frame, num_segments)
            
            if visibility > 0.001:  # Only include visible segments
                partial = segment.partial(visibility)
                # Only include if segment has some length
                if partial.length() > 0.001:
                    visible_segments.append(partial)
        
        return visible_segments
    
    def generate_frames(
        self,
        segments: List[Segment],
        bbox: BoundingBox,
        generator: POVRayGenerator,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[str]:
        """
        Generate all animation frame .pov files.
        
        Args:
            segments: Complete list of segments
            bbox: Bounding box for camera (use full plant bbox)
            generator: POVRayGenerator instance
            progress_callback: Optional callback(current_frame, total_frames)
            
        Returns:
            List of paths to generated .pov files
        """
        pov_files = []
        max_depth = max((seg.depth for seg in segments), default=0)
        
        for frame in range(self.total_frames):
            # Get segments visible at this frame
            frame_segments = self.get_frame_segments(segments, frame)
            
            # Generate POV-Ray scene
            pov_file = generator.generate_frame(
                frame_segments,
                bbox,
                frame,
                max_depth
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
        # More segments = faster individual growth
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
        
        # Only increase if user didn't explicitly set frames and minimum is needed
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
