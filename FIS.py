import fuzzylite as fl
from typing import Iterable, Union, Literal
import matplotlib.pyplot as plt
import numpy as np


class FIS:
    def __init__(
        self,
        name: str = "My FIS",
        description: str = "Fuzzy Inference System",
    ) -> None:
        """
        Create a Fuzzy Inference System using
        the fuzzylite library. This module allows
        you to custom all variables in the FIS.

        Parameters
        __________
        name: str, optional
            Defines the name of the FIS.
        description: str, optional
            Defines the description of the FIS

        Example
        _______
        # Create the FIS
        >>> from FIS import *
        >>> fis = FIS("My FIS", "Fuzzy Inference System")
        >>> print(fis.engine)
            Engine: My FIS
                description: Fuzzy Inference System
        """

        # Create the Fuzzy Engine
        self.engine: fl.Engine = fl.Engine(name, description)

        # Initialize Rule Block List
        self.rule_block: fl.RuleBlock = None

        # Initialize Output Inference
        self.output: Union[int, float] = 0.0

    def create_rule_block(
        self,
        rule_name: str = "",
        rule_description: str = "",
        enabled: bool = True,
        rule_conjunction: fl.TNorm | None = fl.Minimum(),
        rule_disjunction: fl.SNorm | None = fl.Maximum(),
        rule_implication: fl.TNorm | None = fl.AlgebraicProduct(),
        rule_activation: fl.Activation | None = fl.General(),
        rules: Iterable[fl.Rule] | None = None,
    ) -> None:
        """
        Create a rule block with the given parameters.

        Parameters
        __________
        rule_name: str, optional
            Defines the name of the rule block.
        rule_description: str, optional
            Defines the description of the rule block.
        enabled: bool, optional
            Defines if the rule block is enabled.
        rule_conjunction: fl.TNorm, optional
            Defines the conjunction operator. The conjunction operator
            is used to combine the antecedents of the rules with the
            AND operator.
        rule_disjunction: fl.SNorm, optional
            Defines the disjunction operator. The disjunction operator
            is used to combine the antecedents of the rules with the
            OR operator.
        rule_implication: fl.TNorm, optional
            Defines the implication. The implication, in fuzzy logic,
            is the degree of a consequent given an antecedent. It can
            be expressed with IF X THEN Y.
        rule_activation: fl.Activation, optional
            Defines the type of activation for the rules. The activation
            is the process of combining the degree of support of the
            antecedents with the implication to obtain the degree of
            support of the consequent.
        rules: Iterable[fl.Rule], optional
            Defines the rules of the rule block. The rules are the
            basic building blocks of a Fuzzy Inference System. Each
            rule has an antecedent and a consequent. The antecedent
            is a set of conditions that are combined with some of
            the operators defined above. The consequent is the action
            that is taken when the antecedent is satisfied.
        """

        # Set the common rule block value
        self.rule_block = fl.RuleBlock(
            name=rule_name,
            description=rule_description,
            enabled=enabled,
            conjunction=rule_conjunction,
            disjunction=rule_disjunction,
            implication=rule_implication,
            activation=rule_activation,
            rules=rules,
        )

    def add_rule_block(self) -> None:
        """
        Add the rule block to the FIS.
        """
        self.engine.rule_blocks.append(self.rule_block)

    def add_input_variable(self, variable: fl.InputVariable = None) -> None:
        """
        Add an input variable to the FIS.

        Parameters
        __________
        variable: fl.InputVariable, optional
            Defines the input variable to add.
        """

        # Check if the variable name is repeated
        if not self._is_valid_variable_name(
            variable.name,
            self.engine.input_variables,
        ):
            raise ValueError("variable_name's need to be different.")

        self.engine.input_variables.append(variable)

    def add_output_variable(self, variable: fl.OutputVariable = None) -> None:
        """
        Add an output variable to the FIS.

        Parameters
        __________
        variable: fl.OutputVariable, optional
            Defines the output variable to add.
        """

        # Check if the variable name is repeated
        if not self._is_valid_variable_name(
            variable.name,
            self.engine.output_variables,
        ):
            raise ValueError("variable_name's need to be different.")

        self.engine.output_variables.append(variable)

    def _is_valid_variable_name(
        self,
        variable_name: str = "",
        set_variable_name: Iterable = [],
    ) -> bool:
        """
        Helper function to avoid repeated variables in the FIS.

        Parameters
        ----------
        variable_name : str
            The name of the variable to check.
        set_variable_name : Iterable
            The variables already added to the FIS.

        Returns
        -------
        bool
            True if the variable name is valid, False otherwise.
        """

        for i in range(len(set_variable_name)):
            name = set_variable_name[i].name
            if name == variable_name:
                return False

        return True

    def create_output_variable(
        self,
        variable_name: str = "",
        variable_description: str = "",
        enable: bool = True,
        variable_minimum: Union[int, float] = 0,
        variable_maximum: Union[int, float] = 1,
        ratio: float = 0.5,
        lock_range: bool = False,
        aggregation: fl.SNorm | None = fl.Maximum(),
        defuzzifier: fl.Defuzzifier | None = fl.Centroid(50),
        variable_labels: Iterable[fl.Term] = ["low", "average", "high"],
        auto_mf_type: Literal["triangular", "gaussian", "trapezoid"] = None,
        terms: Iterable[fl.Term] = None,
        overlap: Union[int, float] = 0.0,
    ) -> fl.OutputVariable:
        """
        Create an output variable with the given parameters.

        Parameters
        __________

        variable_name: str, optional
            Defines the name of the variable.
        variable_description: str, optional
            Defines the description of the variable.
        enable: bool, optional
            Defines if the variable is enabled.
        variable_minimum: Union[int, float], optional
            Set the minimum value in the variable universe.
        variable_maximum: Union[int, float], optional
            Set the maximum value in the variable universe.
        ratio: float, optional
            In case of using trapezoid membership functions, this
            parameter defines the ratio of the top of the trapezoid.
            For example, 0.5 means that the top of the trapezoid is
            50% of the base and so on.
        lock_range: bool, optional
            Defines if the range of the variable is locked.
        aggregation: fl.SNorm, optional
            Defines the aggregation operator. The aggregation operator
            is used to combine the consequents of the rules with the
            selected operator in the rule block.
        defuzzifier: fl.Defuzzifier, optional
            Defines the defuzzifier. The defuzzifier is the process of
            converting the fuzzy output into a crisp value. The default
            is the centroid method with 50 divisions.
        variable_labels: Iterable[fl.Term], optional
            Defines the labels of the membership functions. For default
            are ["low", "average", "high"], but this is a totally
            customizable parameter.
        auto_mf_type: Literal["triangular", "gaussian", "trapezoid"], optional
            Enables the automatic creation of membership functions. The
            options are triangular, gaussian and trapezoid. This functions are
            equally spaced in the universe of the variable based on the
            number of labels.
        terms: Iterable[fl.Term], optional
            Enables the manual creation of membership functions. If the
            problem requires a specific way of defining the membership
            functions, this is the way to go.
        overlap: Union[int, float], optional
            For all types of automatic membership functions, this parameter
            defines the overlap between the membership functions. For example
            0 means no overlap, 0.5 means 50% of overlap and so on.

        Returns
        _______
        fl.OutputVariable
            Returns the output variable created.
        """

        # Check if the terms where added
        if auto_mf_type == None and terms == None:
            raise ValueError(
                "If none membership functions is declared, terms need to be added."
            )

        # Return the terms added
        if auto_mf_type == None and terms != None:
            return fl.OutputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                aggregation=aggregation,
                defuzzifier=defuzzifier,
                terms=terms,
            )

        # Return Triangular Membership Function
        if auto_mf_type == "triangular":
            return fl.OutputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                aggregation=aggregation,
                defuzzifier=defuzzifier,
                terms=self._create_triangular_mf(
                    variable_labels,
                    variable_minimum,
                    variable_maximum,
                    overlap,
                ),
            )

        # Return Gaussian Membership Function
        if auto_mf_type == "gaussian":
            return fl.OutputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                aggregation=aggregation,
                defuzzifier=defuzzifier,
                terms=self._create_gaussian_mf(
                    variable_labels,
                    variable_minimum,
                    variable_maximum,
                    overlap,
                ),
            )

        # Return Trapezoid Membership Function
        if auto_mf_type == "trapezoid":
            return fl.OutputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                aggregation=aggregation,
                defuzzifier=defuzzifier,
                terms=self._create_trapezoid_mf(
                    variable_labels,
                    variable_minimum,
                    variable_maximum,
                    ratio,
                    overlap,
                ),
            )

    def create_input_variable(
        self,
        variable_name: str = "",
        variable_description: str = "",
        enable: bool = True,
        variable_minimum: Union[int, float] = 0,
        variable_maximum: Union[int, float] = 1,
        ratio: float = 0.5,
        lock_range: bool = False,
        variable_labels: Iterable[fl.Term] = ["low", "average", "high"],
        auto_mf_type: Literal["triangular", "gaussian", "trapezoid"] = None,
        terms: Iterable[fl.Term] = None,
        overlap: Union[int, float] = 0.0,
    ) -> fl.InputVariable:
        """
        Create an input variable with the given parameters.

        Parameters
        __________

        variable_name: str, optional
            Defines the name of the variable.
        variable_description: str, optional
            Defines the description of the variable.
        enable: bool, optional
            Defines if the variable is enabled.
        variable_minimum: Union[int, float], optional
            Set the minimum value in the variable universe.
        variable_maximum: Union[int, float], optional
            Set the maximum value in the variable universe.
        ratio: float, optional
            In case of using trapezoid membership functions, this
            parameter defines the ratio of the top of the trapezoid.
            For example, 0.5 means that the top of the trapezoid is
            50% of the base and so on.
        lock_range: bool, optional
            Defines if the range of the variable is locked.
        variable_labels: Iterable[fl.Term], optional
            Defines the labels of the membership functions. For default
            are ["low", "average", "high"], but this is a totally
            customizable parameter.
        auto_mf_type: Literal["triangular", "gaussian", "trapezoid"], optional
            Enables the automatic creation of membership functions. The
            options are triangular, gaussian and trapezoid. This functions are
            equally spaced in the universe of the variable based on the
            number of labels.
        terms: Iterable[fl.Term], optional
            Enables the manual creation of membership functions. If the
            problem requires a specific way of defining the membership
            functions, this is the way to go.
        overlap: Union[int, float], optional
            For all types of automatic membership functions, this parameter
            defines the overlap between the membership functions. For example
            0 means no overlap, 0.5 means 50% of overlap and so on.

        Returns
        _______
        fl.InputVariable
            Returns the input variable created.
        """

        # Check if the terms where added
        if auto_mf_type == None and terms == None:
            raise ValueError(
                "If none membership functions is declared, terms need to be added."
            )

        # Return the terms added
        if auto_mf_type == None and terms != None:
            return fl.InputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                terms=terms,
            )

        # Return Triangular Membership Function
        if auto_mf_type == "triangular":
            return fl.InputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                terms=self._create_triangular_mf(
                    variable_labels,
                    variable_minimum,
                    variable_maximum,
                    overlap,
                ),
            )

        # Return Gaussian Membership Function
        if auto_mf_type == "gaussian":
            return fl.InputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                terms=self._create_gaussian_mf(
                    variable_labels,
                    variable_minimum,
                    variable_maximum,
                    overlap,
                ),
            )

        # Return Trapezoid Membership Function
        if auto_mf_type == "trapezoid":
            return fl.InputVariable(
                name=variable_name,
                description=variable_description,
                enabled=enable,
                minimum=variable_minimum,
                maximum=variable_maximum,
                lock_range=lock_range,
                terms=self._create_trapezoid_mf(
                    variable_labels,
                    variable_minimum,
                    variable_maximum,
                    ratio,
                    overlap,
                ),
            )

    def _create_gaussian_mf(
        self,
        labels: Iterable[fl.Term] = ["low", "average", "high"],
        minimum: Union[int, float] = 0,
        maximum: Union[int, float] = 1,
        overlap: Union[int, float] = 0,
    ) -> Iterable[fl.Gaussian]:
        """
        Helper function to create Gaussian membership functions.

        Parameters
        ----------
        labels : Iterable[fl.Term], optional
            The labels of the membership functions.
        minimum : Union[int, float], optional
            The minimum value of the universe of the variable.
        maximum : Union[int, float], optional
            The maximum value of the universe of the variable.
        overlap : Union[int, float], optional
            The overlap between the membership functions.

        Returns
        -------
        Iterable[fl.Gaussian]
            The Gaussian membership functions created.

        Mathematical Explanation
        ------------------------

        For visualization, we'll use this triangular representation
        as a Gaussian-like function.
             B
            / \
           /   \
          /     \
         /       \
        A---------C

        Based on the properties of the Gaussian function, we can
        define the mean of the function as:
            mean = b
        
        The standard deviation is completely dependent on where is, but
        the main trouble is how to calculated, well, based on the figure
        and knowing that in 3*std_dev we have 99.7% of the data, we can
        define the standard deviation as:
            std_dev = (mean - c) / 3 (for right side)
            std_dev = (mean - a) / 3 (for left side)
        """

        n = len(labels)
        range_size = maximum - minimum
        step = range_size / n

        mfs = []
        for i, label in enumerate(labels):
            if i == 0:
                c = minimum + step * (1 + overlap)
                mean = minimum
                std_dev = (mean - c) / 3

            elif i == n - 1:
                a = minimum + step * (i - overlap)
                mean = maximum
                std_dev = (mean - a) / 3
            else:
                a = minimum + step * (i + 0 - overlap)
                c = minimum + step * (i + 1 + overlap)
                b = 0.5 * (c + a)
                mean = b
                std_dev = (mean - c) / 3

            mfs.append(fl.Gaussian(label, mean, std_dev))

        return mfs

    def _create_trapezoid_mf(
        self,
        labels: Iterable[fl.Term] = ["low", "average", "high"],
        minimum: Union[int, float] = 0,
        maximum: Union[int, float] = 1,
        ratio: float = 0.5,
        overlap: Union[int, float] = 0,
    ) -> Iterable[fl.Trapezoid]:
        """
        Helper function to create Gaussian membership functions.

        Parameters
        ----------
        labels : Iterable[fl.Term], optional
            The labels of the membership functions.
        minimum : Union[int, float], optional
            The minimum value of the universe of the variable.
        maximum : Union[int, float], optional
            The maximum value of the universe of the variable.
        ratio : float, optional
            The ratio of the top of the trapezoid. For example, 0.5
            means that the top of the trapezoid is 50% of the base.
        overlap : Union[int, float], optional
            The overlap between the membership functions.

        Returns
        -------
        Iterable[fl.Trapezoid]
            The Trapezoid membership functions created.

        Mathematical Explanation
        ------------------------

        For visualization, we'll use this trapezoid representation.
             B______C
            /        \
           /          \
          /            \
         /              \
        A----------------D

        Based on the geometrical properties of the Trapezoid, the A point
        is the minimum value in the label, the C point is the maximum
        value in the label.
        For calculate the values of B and C points, we need to stablish a 
        ratio between top side and bottom side, and calculate the half of 
        that lenght to add it or substract it dependes of the point:
            half_top = ratio * (D - A) * 0.5
            mid = (D + A) * 0.5
        From the middle point of the trapezoid, for B point:
            B = mid - half_top
        From the middle point of the trapezoid, for C point:
            C = mid + half_top
        The ration can be expressed as:
            ratio = BC / AD
        """

        n = len(labels)
        range_size = maximum - minimum
        step = range_size / n

        mfs = []
        for i, label in enumerate(labels):
            if i == 0:
                a = minimum
                b = minimum
                d = minimum + step * (1 + overlap)
                half_top = ratio * (d - a)
                c = minimum + half_top
            elif i == n - 1:
                a = minimum + step * (i - overlap)
                c = maximum
                d = maximum
                b = (a + d) * ratio
            else:
                a = minimum + step * (i + 0 - overlap)
                d = minimum + step * (i + 1 + overlap)
                mid = (d + a) * 0.5
                # ratio * (d - a) # size of top side
                # (d - a)         # size of bottom side
                half_top = ratio * (d - a) * 0.5
                b = mid - half_top
                c = mid + half_top

            mfs.append(fl.Trapezoid(label, a, b, c, d))

        return mfs

    def _create_triangular_mf(
        self,
        labels: Iterable[fl.Term] = ["low", "average", "high"],
        minimum: Union[int, float] = 0,
        maximum: Union[int, float] = 1,
        overlap: Union[int, float] = 0,
    ) -> Iterable[fl.Triangle]:
        """
        Helper function to create Gaussian membership functions.

        Parameters
        ----------
        labels : Iterable[fl.Term], optional
            The labels of the membership functions.
        minimum : Union[int, float], optional
            The minimum value of the universe of the variable.
        maximum : Union[int, float], optional
            The maximum value of the universe of the variable.
        overlap : Union[int, float], optional
            The overlap between the membership functions.

        Returns
        -------
        Iterable[fl.Triangle]
            The Triangle membership functions created.

        Mathematical Explanation
        ------------------------

        For visualization, we'll use this triangular representation.
             B
            / \
           /   \
          /     \
         /       \
        A---------C

        Based on the geometrical properties of the Triangle, the A point
        is the minimum value in the label, the C point is the maximum
        value in the label and the B point is the middle value between
        A and C.
        """

        n = len(labels)
        range_size = maximum - minimum
        step = range_size / n

        mfs = []
        for i, label in enumerate(labels):
            if i == 0:
                a = minimum
                b = minimum
                c = minimum + step * (1 + overlap)
            elif i == n - 1:
                a = minimum + step * (i - overlap)
                b = maximum
                c = maximum
            else:
                a = minimum + step * (i + 0 - overlap)
                c = minimum + step * (i + 1 + overlap)
                b = 0.5 * (c + a)

            mfs.append(fl.Triangle(label, a, b, c))

        return mfs

    def add_rules_from_list(self, rule_list: Iterable[str] = None) -> None:
        """
        Add rules to the rule block from a given set of rules.

        Parameters
        __________
        rule_list: Iterable[str]
            Set of rules given as an array of strings.

        Example
        _______
            my_rules = ["if var1 is low then out1 is high", "if var2 is high then out1 is low",]
        """
        # Clear the rules in the rule blocks
        self.rule_block.rules = []

        # Assign the rules to the rule_block
        for rule in rule_list:
            self.rule_block.rules.append(fl.Rule.create(rule, self.engine))

    def inference(self, inputs: Iterable[Union[int, float]] = None) -> None:
        # Assign the input variables
        n = len(inputs)
        inputs_name = self.get_input_variable_names()
        for i in range(n):
            str_input = inputs_name[i]
            self.engine.input_variable(str_input).value = inputs[i]

        # Do the inference
        self.engine.process()

        # Assign the output variables
        output_name = self.get_output_variable_names()
        self.output = self.engine.output_variable(output_name[0]).value

    def get_input_variable_names(self) -> Iterable[str]:
        """
        Get the name of the output variables.
        """
        # How many input variables?
        n = len(self.engine.input_variables)

        # Save names
        names = []
        for i in range(n):
            names.append(self.engine.input_variables[i].name)

        # Return names
        return names

    def get_output_variable_names(self) -> Iterable[str]:
        """
        Get the name of the input variables.
        """
        # How many output variables?
        n = len(self.engine.output_variables)

        # Save names
        names = []
        for i in range(n):
            names.append(self.engine.output_variables[i].name)

        # Return names
        return names

    # JUST FOR VISUALIZATION, THIS CAN BE CUSTOMIZED

    def plot_membership_functions(self, variable_name: str) -> None:
        """
        Plot the membership functions of a given variable.

        Parameters
        ----------
        variable_name : str
            The name of the variable to plot.
        """
        variable = self.engine.variable(variable_name)

        fig, ax = plt.subplots()
        for term in variable.terms:
            term_values = [
                term.membership(x)
                for x in np.linspace(variable.minimum, variable.maximum, 100)
            ]
            ax.plot(
                np.linspace(variable.minimum, variable.maximum, 100),
                term_values,
                label=term.name,
            )

        ax.set_title(f"Membership Functions of {variable_name}")
        ax.set_xlabel("Values")
        ax.set_ylabel("Membership")
        ax.legend()
        plt.show()

    def plot_all_inputs(self) -> None:
        """
        Plot the membership functions of all input variables.
        """
        n = len(self.engine.input_variables)
        fig, axs = plt.subplots(n, 1, figsize=(8, 3 * n))

        if n == 1:
            axs = [axs]  # Ensure axs is iterable

        for i, variable in enumerate(self.engine.input_variables):
            variable_name = variable.name
            for term in variable.terms:
                term_values = [
                    term.membership(x)
                    for x in np.linspace(variable.minimum, variable.maximum, 100)
                ]
                axs[i].plot(
                    np.linspace(variable.minimum, variable.maximum, 100),
                    term_values,
                    label=term.name,
                )
            axs[i].set_title(f"Membership Functions of {variable_name}")
            axs[i].set_xlabel("Values")
            axs[i].set_ylabel("Membership")
            axs[i].legend()

        plt.tight_layout()
        plt.show()

    def plot_all_outputs(self) -> None:
        """
        Plot the membership functions of all output variables.
        """
        n = len(self.engine.output_variables)
        fig, axs = plt.subplots(n, 1, figsize=(8, 3 * n))

        if n == 1:
            axs = [axs]  # Ensure axs is iterable

        for i, variable in enumerate(self.engine.output_variables):
            variable_name = variable.name
            for term in variable.terms:
                term_values = [
                    term.membership(x)
                    for x in np.linspace(variable.minimum, variable.maximum, 100)
                ]
                axs[i].plot(
                    np.linspace(variable.minimum, variable.maximum, 100),
                    term_values,
                    label=term.name,
                )
            axs[i].set_title(f"Membership Functions of {variable_name}")
            axs[i].set_xlabel("Values")
            axs[i].set_ylabel("Membership")
            axs[i].legend()

        plt.tight_layout()
        plt.show()

    def plot_all_variables(self) -> None:
        """
        Plot the membership functions of all input and output variables together.
        """
        n_inputs = len(self.engine.input_variables)
        n_outputs = len(self.engine.output_variables)
        total_vars = n_inputs + n_outputs
        # fig, axs = plt.subplots(total_vars, 1, figsize=(8, 2.5 * total_vars))
        fig, axs = plt.subplots(1, total_vars, figsize=(6 * total_vars, 4))

        if total_vars == 1:
            axs = [axs]  # Ensure axs is iterable

        # Plot input variables
        for i, variable in enumerate(self.engine.input_variables):
            variable_name = variable.name
            for term in variable.terms:
                term_values = [
                    term.membership(x)
                    for x in np.linspace(variable.minimum, variable.maximum, 100)
                ]
                axs[i].plot(
                    np.linspace(variable.minimum, variable.maximum, 100),
                    term_values,
                    label=term.name,
                )
            axs[i].set_title(f"Membership Functions of {variable_name} (Input)")
            axs[i].set_xlabel("Values")
            axs[i].set_ylabel("Membership")
            axs[i].legend()

        # Plot output variables
        for i, variable in enumerate(self.engine.output_variables):
            variable_name = variable.name
            for term in variable.terms:
                term_values = [
                    term.membership(x)
                    for x in np.linspace(variable.minimum, variable.maximum, 100)
                ]
                axs[n_inputs + i].plot(
                    np.linspace(variable.minimum, variable.maximum, 100),
                    term_values,
                    label=term.name,
                )
            axs[n_inputs + i].set_title(
                f"Membership Functions of {variable_name} (Output)"
            )
            axs[n_inputs + i].set_xlabel("Values")
            axs[n_inputs + i].set_ylabel("Membership")
            axs[n_inputs + i].legend()

        plt.tight_layout()
        plt.show()
