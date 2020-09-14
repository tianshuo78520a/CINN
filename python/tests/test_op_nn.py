#!/usr/bin/env python3
import unittest
import math
import numpy as np
import cinn
from cinn import frontend
from cinn import runtime
from cinn import lang
from cinn import framework
from cinn import ir
from cinn import common
from cinn.poly import create_stages
import logging
from test_utils import SingleOpTester
import pool_utils


class OpTest_relu(SingleOpTester):
    def create_target_data(self, inputs_data):
        [X] = inputs_data
        return np.maximum(X, np.zeros(X.shape).astype("float32"))

    def test_op(self):
        attrs = framework.NodeAttr()
        self.to_test_op([[32]], [[32]], "relu", attrs)


class OpTest_relu6(SingleOpTester):
    def create_target_data(self, inputs_data):
        [X] = inputs_data
        return np.minimum(
            np.maximum(X,
                       np.zeros(np.array(X).shape).astype("float32")), 6)

    def test_op(self):
        attrs = framework.NodeAttr()
        self.to_test_op([[32, 32]], [[32, 32]], "relu6", attrs)


""" class OpTest_conv2d(SingleOpTester):
    def create_target_data(self, inputs_data):
        return np.ones((1, 2, 5, 5)).astype("float32")

    def test_op(self):
        attrs = framework.NodeAttr()
        attrs.attr_store = {"padding": [1, 1]}
        attrs.set_attr("stride", [2, 2])
        attrs.set_attr("dilation", 2)
        attrs.set_attr("groups", 1)
        self.to_test_op([[1, 3, 10, 10], [2, 3, 2, 2]],
                        [[1, 3, 12, 12], [2, 3, 3, 3], [1, 2, 5, 5]], "conv2d", attrs) """


class OpTest_pool1d(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2],
        "stride_size": [2],
        "padding_size": [1, 1],
        "pool_type": "max",
        "ceil_mode": False,
        "exclusive": True,
        "data_format": "NCW"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool1d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 3, 8]
        self.to_test_op([input_shape], None, "pool1d", self.attrs)


class OpTest_pool1d_1(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2],
        "stride_size": [2],
        "padding_size": [2, 3],
        "pool_type": "avg",
        "ceil_mode": False,
        "exclusive": True,
        "data_format": "NCW"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool1d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 3, 8]
        self.to_test_op([input_shape], None, "pool1d", self.attrs)


class OpTest_pool1d_2(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2],
        "stride_size": [3],
        "padding_size": [4, 5],
        "pool_type": "avg",
        "ceil_mode": True,
        "exclusive": False,
        "data_format": "NWC"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool1d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 8, 3]
        self.to_test_op([input_shape], None, "pool1d", self.attrs)


class OpTest_pool2d(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2, 2],
        "stride_size": [2, 2],
        "padding_size": [1, 1, 1, 1],
        "pool_type": "max",
        "ceil_mode": False,
        "exclusive": True,
        "data_format": "NCHW"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool2d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 3, 8, 8]
        self.to_test_op([input_shape], None, "pool2d", self.attrs)


class OpTest_pool2d_1(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2, 2],
        "stride_size": [2, 2],
        "padding_size": [2, 3, 4, 5],
        "pool_type": "avg",
        "ceil_mode": False,
        "exclusive": True,
        "data_format": "NCHW"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool2d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 3, 8, 8]
        self.to_test_op([input_shape], None, "pool2d", self.attrs)


class OpTest_pool2d_2(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2, 2],
        "stride_size": [3, 3],
        "padding_size": [2, 3, 4, 5],
        "pool_type": "avg",
        "ceil_mode": True,
        "exclusive": False,
        "data_format": "NHWC"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool2d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 8, 8, 3]
        self.to_test_op([input_shape], None, "pool2d", self.attrs)


class OpTest_pool3d(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2, 2, 2],
        "stride_size": [2, 2, 2],
        "padding_size": [1, 2, 3, 4, 5, 6],
        "pool_type": "max",
        "ceil_mode": False,
        "exclusive": True,
        "data_format": "NCDHW"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool3d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [2, 3, 8, 8, 8]
        self.to_test_op([input_shape], None, "pool3d", self.attrs)


class OpTest_pool3d_1(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2, 2, 2],
        "stride_size": [2, 2, 2],
        "padding_size": [1, 1, 1, 1, 1, 1],
        "pool_type": "avg",
        "ceil_mode": False,
        "exclusive": True,
        "data_format": "NCDHW"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool3d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 3, 8, 8, 8]
        self.to_test_op([input_shape], None, "pool3d", self.attrs)


class OpTest_pool3d_2(SingleOpTester):
    attrs = framework.NodeAttr()
    attrs.attr_store = {
        "kernel_size": [2, 2, 2],
        "stride_size": [2, 2, 2],
        "padding_size": [1, 2, 3, 4, 5, 6],
        "pool_type": "avg",
        "ceil_mode": True,
        "exclusive": False,
        "data_format": "NDHWC"
    }

    def create_target_data(self, inputs_data):
        return pool_utils.pool3d(inputs_data[0], self.attrs)

    def test_op(self):
        input_shape = [1, 8, 8, 8, 3]
        self.to_test_op([input_shape], None, "pool3d", self.attrs)


class OpTest_batchnorm(SingleOpTester):
    def create_target_data(self, inputs_data):
        [X, Y] = inputs_data
        c = X.shape[1]
        for i in range(0, c):
            X[:, i, :, :] = (X[:, i, :, :] - Y[0, i]) / math.sqrt(
                Y[1, i] + 0.00001) * Y[2, i] + Y[3, i]
        return X

    def test_op(self):
        attrs = framework.NodeAttr()
        self.to_test_op([[1, 3, 2, 2], [4, 3]], [[1, 3, 2, 2]], "batchnorm",
                        attrs)


if __name__ == "__main__":
    unittest.main()