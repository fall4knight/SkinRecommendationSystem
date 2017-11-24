#!/usr/bin/python
#-*-coding=utf8-*-


import numpy as np
import pandas as pd


class Recommender:
    def __init__(self, mat, item_list, feature_list):
        """
        Initialize
        """
        self.mat = mat
        self.normalized_mat = self.mat / np.linalg.norm(self.mat, axis=1)[:, None]
        self.item_list = item_list
        self.feature_list = feature_list
        #print(self.mat)
        #print(self.normalized_mat)
        """
        item_to_index : item索引
        feature_to_index : feature索引
        """
        self.item_to_index = {item: index for index, item in enumerate(item_list)}
        self.feature_to_index = {feature: index for index, feature in enumerate(feature_list)}
        """
        检查mat格式
        """
        if mat.shape != (len(item_list), len(feature_list)):
            raise "Input matrix shape is not compatible with item_list, feature_list"
        self.sim_mat = self.normalized_mat * self.normalized_mat.transpose()
        np.fill_diagonal(self.sim_mat, 0)
        #print(self.sim_mat)



    def recommend(self, item_arr, ret_size = 0):
        """
        @param item_arr: 用户的安装的皮肤列表
        @param ret_size: 返回推荐皮肤数量
        @return 推荐的皮肤列表
        """
        if ret_size >= len(self.item_list) or ret_size <= 0:
            ret_size = len(self.item_list)
        # 将item_arr转换为index_arr : 使用item_to_index
        for item in item_arr:
            if item in self.item_list:
                index_arr = self.item_to_index[item]
        if len(item_arr) == 0:
            raise 'Packages input ERROR!'
        #index_arr = [self.item_to_index[item] for item in item_arr]
        # 从self.sim_mat中按照index_arr选择这么多列
        mat = self.sim_mat[:, index_arr]
        # 假设我们是求平均的相似度。
        mean_sim = mat.mean(axis=1).flatten()
        # 然后选平均的相似度最高的ret_size个
        #ret_index_arr = mean_sim.argpartition(mean_sim.shape[0] - ret_size)[-ret_size:]
        #return [self.item_list[index] for index in ret_index_arr]
        ret_index_arr = np.argsort(-mean_sim).tolist()
        #ret_index_arr = np.argpartition(-mean_sim, ret_size).tolist()
        #print(ret_index_arr[0][:ret_size])
        ret_item_arr = [self.item_list[index] for index in ret_index_arr[0][:(ret_size+len(item_arr))]]
        #return ret_index_arr[0][:ret_size]
        #print(ret_item_arr.type)
        for i in range(len(ret_item_arr)):
            if ret_item_arr[i] in item_arr:
                ret_item_arr[i] = ''
        ret_item_arr = [i for i in ret_item_arr if i != '']

        return ret_item_arr



    @classmethod
    def build(cls, filename):
        """
        输入文件每一行是skin及其tags
        @param filename: skin及其标记的feature的文件
        @return Recommender对象
        """
        item_list = []
        feature_list = []
        feature_to_index = {}
        data = {}
        with open(filename) as f:
            for item_index, line in enumerate(f):
                items = line.strip().split('\t')
                item_list.append(items[0])
                del items[0]
                feature_dict = {}
                for x in items:
                    #print(items)
                    feature, val = x.split(":")
                    if feature in feature_to_index:
                        feature_index = feature_to_index[feature]
                    else:
                        feature_index = len(feature_to_index)
                        feature_to_index[feature] = feature_index
                        feature_list.append(feature)
                    feature_dict[feature_index] = float(val)        # feature_index -- val权重
                data[item_index] = feature_dict
        df = pd.DataFrame.from_dict(data, orient='index')
        matrix  = np.matrix(df)
        matrix[np.isnan(matrix)] = 0
        return Recommender(matrix, item_list, feature_list)


if __name__ == "__main__":
    recommender = Recommender.build("skin_features.csv")
    recommended_list = recommender.recommend(["com.cootek.smartinputv5.skin.keyboard_theme_new_enjoy_life", "com.cootek.smartinputv5.skin.keyboard_theme_pitbull", "com.cootek.smartinputv5.skin.keyboard_theme_color_glass"], 5)
    print('\n'.join(recommended_list))
