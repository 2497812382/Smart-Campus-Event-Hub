<template>
	<view>
		<view class="uni-header">
			<view class="uni-group">
				<!-- 显示标题 -->
				<view class="uni-title">{{$t('demo.icons.title')}}（uni-icons）</view>
				<!-- 显示描述 -->
				<view class="uni-sub-title">{{$t('demo.icons.describle')}}</view>
			</view>
		</view>
		    <!-- 表格 -->
		    <view class="table-container">
		      <view v-for="(item, index) in highPopularityEvents" :key="index" class="event-item">
		        <!-- 图片 -->
		        <view class="event-image">
		          <!-- 使用 item.image 作为图片路径 -->
		          <image :src="item.image" mode="aspectFit"></image>
		        </view>
		        <!-- 活动名称 -->
		        <view class="event-name">{{ item.name }}</view>
		        <!-- 详情按钮 -->
		        <button class="detail-button" @click="showDetail(item)">{{ $t('common.button.detail') }}</button>
		      </view>
		    </view>
	</view>
</template>

<script>
// 导入 tableData
import tableData from '../table/tableData.js';

export default {
  data() {
    return {
      highPopularityEvents: []
    };
  },
  onLoad() {
    // 筛选出 popularity 为 "high" 的活动
    this.highPopularityEvents = tableData.filter(item => item.popularity === 'high');
  },
  methods: {
    showDetail(item) {
      // 这里可以添加查看详情的逻辑
      console.log('查看详情:', item);
    }
  }
};
</script>

<style scoped>
.table-container {
  padding: 10px;
}

.event-item {
  background-color: #f5f5f5; /* 浅灰色背景 */
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.event-image {
  width: 100px; /* 设置图片容器的宽度 */
  height: 100px; /* 设置图片容器的高度 */
  margin-right: 10px;
  overflow: hidden; /* 确保图片超出容器部分隐藏 */
}

.event-image image {
  max-width: 100%; /* 图片最大宽度不超过容器宽度 */
  max-height: 100%; /* 图片最大高度不超过容器高度 */
  object-fit: cover; /* 保持图片比例并覆盖容器 */
}

.event-name {
  flex: 1; /* 让活动名称占据剩余空间 */
  font-size: 16px;
  margin-right: 10px; /* 与详情按钮保持一定间距 */
}

.detail-button {
  padding: 5px 10px;
  background-color: #007aff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>

