"""
Tests for Parametric L-System Engine

Tests the ABOP-style parametric L-system features:
- Parameterized modules
- Conditional productions
- Stochastic selection
- Expression evaluation
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lsystem.parametric import (
    Module, 
    Production, 
    ParametricLSystem,
    parse_parametric_word, 
    parse_production_string,
    parse_stochastic_production,
    _eval_expr
)


class TestModule:
    """Tests for Module class."""
    
    def test_basic_module(self):
        """Test creating a module with parameters."""
        m = Module("A", (1.0, 2.0))
        assert m.symbol == "A"
        assert m.params == (1.0, 2.0)
        assert "A(1,2)" in repr(m)
    
    def test_no_params(self):
        """Test module without parameters."""
        m = Module("F")
        assert m.symbol == "F"
        assert m.params == ()
        assert repr(m) == "F"
    
    def test_single_param(self):
        """Test module with single parameter."""
        m = Module("F", (10.5,))
        assert m.params == (10.5,)
        assert "10.5" in repr(m)
    
    def test_module_equality(self):
        """Test module equality comparison."""
        m1 = Module("A", (1.0, 2.0))
        m2 = Module("A", (1.0, 2.0))
        m3 = Module("A", (1.0, 3.0))
        m4 = Module("B", (1.0, 2.0))
        
        assert m1 == m2
        assert m1 != m3
        assert m1 != m4
    
    def test_matches_symbol(self):
        """Test symbol matching."""
        m = Module("A", (1.0, 2.0))
        assert m.matches_symbol("A")
        assert m.matches_symbol("A", param_count=2)
        assert not m.matches_symbol("B")
        assert not m.matches_symbol("A", param_count=3)


class TestParseWord:
    """Tests for parse_parametric_word function."""
    
    def test_simple(self):
        """Test parsing simple word."""
        modules = parse_parametric_word("AB")
        assert len(modules) == 2
        assert modules[0].symbol == "A"
        assert modules[1].symbol == "B"
    
    def test_parameterized(self):
        """Test parsing parameterized modules."""
        modules = parse_parametric_word("A(1,2)F(3)")
        assert len(modules) == 2
        assert modules[0] == Module("A", (1.0, 2.0))
        assert modules[1] == Module("F", (3.0,))
    
    def test_mixed(self):
        """Test parsing mixed word."""
        modules = parse_parametric_word("F(1)[+A(2)]")
        assert len(modules) == 5
        assert modules[0] == Module("F", (1.0,))
        assert modules[1] == Module("[")
        assert modules[2] == Module("+")
        assert modules[3] == Module("A", (2.0,))
        assert modules[4] == Module("]")
    
    def test_expression_substitution(self):
        """Test parameter substitution in expressions."""
        modules = parse_parametric_word("F(l*0.9)", {"l": 10})
        assert len(modules) == 1
        assert abs(modules[0].params[0] - 9.0) < 0.01
    
    def test_complex_expression(self):
        """Test complex expression evaluation."""
        modules = parse_parametric_word("A(sqrt(16),x+y)", {"x": 3, "y": 2})
        assert abs(modules[0].params[0] - 4.0) < 0.01
        assert abs(modules[0].params[1] - 5.0) < 0.01
    
    def test_special_symbols(self):
        """Test parsing special ABOP symbols."""
        modules = parse_parametric_word("!$.'{}%")
        symbols = [m.symbol for m in modules]
        assert "!" in symbols
        assert "$" in symbols
        assert "." in symbols
        assert "'" in symbols
        assert "{" in symbols
        assert "}" in symbols
        assert "%" in symbols


class TestProduction:
    """Tests for Production class."""
    
    def test_condition_true(self):
        """Test production condition evaluation (true)."""
        prod = Production("A", ("x",), "x > 5", "B")
        params = {"x": 10}
        assert prod.matches(Module("A", (10,)), params)
    
    def test_condition_false(self):
        """Test production condition evaluation (false)."""
        prod = Production("A", ("x",), "x > 5", "B")
        params = {"x": 3}
        assert not prod.matches(Module("A", (3,)), params)
    
    def test_no_condition(self):
        """Test production without condition."""
        prod = Production("A", ("x",), None, "B(x)")
        params = {"x": 10}
        assert prod.matches(Module("A", (10,)), params)
    
    def test_apply(self):
        """Test production application."""
        prod = Production("A", ("x",), None, "B(x+1)")
        result = prod.apply({"x": 5})
        assert len(result) == 1
        assert result[0].symbol == "B"
        assert abs(result[0].params[0] - 6.0) < 0.01
    
    def test_complex_condition(self):
        """Test complex condition with math functions."""
        prod = Production("A", ("x", "y"), "x > y and x < 10", "B")
        assert prod.matches(Module("A", (5, 3)), {"x": 5, "y": 3})
        assert not prod.matches(Module("A", (5, 7)), {"x": 5, "y": 7})


class TestParseProductionString:
    """Tests for parse_production_string function."""
    
    def test_simple(self):
        """Test parsing simple production."""
        prod = parse_production_string("F -> FF")
        assert prod.predecessor == "F"
        assert prod.successor == "FF"
        assert prod.formal_params == ()
        assert prod.condition is None
    
    def test_with_params(self):
        """Test parsing production with parameters."""
        prod = parse_production_string("A(x,y) -> B(x+1)C(y)")
        assert prod.predecessor == "A"
        assert prod.formal_params == ("x", "y")
        assert prod.successor == "B(x+1)C(y)"
    
    def test_with_condition(self):
        """Test parsing production with condition."""
        prod = parse_production_string("A(x) : x > 5 -> B(x-1)")
        assert prod.predecessor == "A"
        assert prod.formal_params == ("x",)
        assert prod.condition == "x > 5"
        assert prod.successor == "B(x-1)"
    
    def test_unicode_arrow(self):
        """Test parsing with Unicode arrow."""
        prod = parse_production_string("A(x) : x > 5 → B(x-1)")
        assert prod.predecessor == "A"
        assert prod.condition == "x > 5"


class TestParametricLSystem:
    """Tests for ParametricLSystem class."""
    
    def test_simple_growth(self):
        """Test simple parametric growth."""
        prods = [
            Production("A", ("l",), "l < 10", "F(l)A(l+1)"),
            Production("A", ("l",), "l >= 10", "F(l)"),
        ]
        lsys = ParametricLSystem("A(1)", prods, iterations=5)
        result = lsys.generate()
        
        # Should have 5 F modules and final A
        f_count = sum(1 for m in result if m.symbol == "F")
        assert f_count == 5
    
    def test_stochastic(self):
        """Test stochastic production selection."""
        prods = [
            Production("F", (), None, "FF", probability=0.5),
            Production("F", (), None, "F", probability=0.5),
        ]
        lsys = ParametricLSystem("F", prods, iterations=10, random_seed=42)
        result1 = lsys.to_string()
        
        # Reset and regenerate
        lsys.reset_random()
        result2 = lsys.to_string(lsys.generate())
        
        # Same seed should give same result
        assert result1 == result2
    
    def test_constants(self):
        """Test named constants."""
        prods = [
            Production("A", ("l",), None, "F(l*R)A(l*R)"),
        ]
        lsys = ParametricLSystem("A(10)", prods, iterations=3, 
                                 constants={"R": 0.5})
        result = lsys.generate()
        
        # Check that constant was applied
        # A(10) → F(5)A(5) → F(5)F(2.5)A(2.5) → F(5)F(2.5)F(1.25)A(1.25)
        f_params = [m.params[0] for m in result if m.symbol == "F"]
        assert len(f_params) == 3
        assert abs(f_params[0] - 5.0) < 0.01   # 10 * 0.5
        assert abs(f_params[1] - 2.5) < 0.01   # 5 * 0.5
        assert abs(f_params[2] - 1.25) < 0.01  # 2.5 * 0.5
    
    def test_to_string(self):
        """Test conversion to turtle string."""
        prods = [
            Production("A", ("l",), None, "F[+A(l)][-A(l)]"),
        ]
        lsys = ParametricLSystem("A(1)", prods, iterations=2)
        result = lsys.to_string()
        
        # Should contain F, [, ], +, -
        assert "F" in result
        assert "[" in result
        assert "]" in result
    
    def test_get_module_params(self):
        """Test getting parameter values by position."""
        prods = [
            Production("A", ("l",), None, "F(l)A(l*2)"),
        ]
        lsys = ParametricLSystem("A(1)", prods, iterations=3)
        result = lsys.generate()
        params = lsys.get_module_params(result)
        
        # Should have params for F and A modules
        assert len(params) > 0
    
    def test_max_modules_limit(self):
        """Test that max modules limit is enforced."""
        # Create a rule that grows exponentially
        prods = [
            Production("A", (), None, "AA"),
        ]
        lsys = ParametricLSystem("A", prods, iterations=100)
        
        with pytest.raises(Exception):  # Should raise error
            lsys.generate()
    
    def test_no_matching_production(self):
        """Test that modules without productions persist."""
        prods = [
            Production("A", (), None, "FB"),
        ]
        lsys = ParametricLSystem("AX", prods, iterations=1)
        result = lsys.generate()
        
        # X should persist since no production matches
        assert any(m.symbol == "X" for m in result)


class TestExpressionEvaluation:
    """Tests for expression evaluation."""
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic."""
        assert abs(_eval_expr("2+3", {}) - 5) < 0.01
        assert abs(_eval_expr("10/2", {}) - 5) < 0.01
        assert abs(_eval_expr("3*4", {}) - 12) < 0.01
    
    def test_parameter_substitution(self):
        """Test parameter substitution."""
        assert abs(_eval_expr("x+1", {"x": 5}) - 6) < 0.01
        assert abs(_eval_expr("x*y", {"x": 3, "y": 4}) - 12) < 0.01
    
    def test_math_functions(self):
        """Test math function evaluation."""
        import math
        assert abs(_eval_expr("sqrt(16)", {}) - 4) < 0.01
        assert abs(_eval_expr("sin(0)", {}) - 0) < 0.01
        assert abs(_eval_expr("pi", {}) - math.pi) < 0.01


class TestStochasticProductions:
    """Tests for stochastic production behavior."""
    
    def test_distribution(self):
        """Test that stochastic selection follows probabilities."""
        prods = [
            Production("F", (), None, "A", probability=0.7),
            Production("F", (), None, "B", probability=0.3),
        ]
        
        # Run multiple times and count results
        a_count = 0
        b_count = 0
        trials = 100
        
        for i in range(trials):
            lsys = ParametricLSystem("F", prods, iterations=1, random_seed=i)
            result = lsys.to_string()
            if "A" in result:
                a_count += 1
            elif "B" in result:
                b_count += 1
        
        # Should roughly follow 70/30 distribution
        # Allow some variance since it's random
        assert a_count > b_count  # A should be more common


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
