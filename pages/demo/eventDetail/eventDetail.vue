<!-- pages/demo/eventDetail/eventDetail.vue -->
<template>
  <view class="container">
    <view v-if="eventDetail">
      <view>
        <text>活动标题: </text>
        <text>{{ eventDetail.name }}</text>
      </view>
      <view>
        <text>活动时间: </text>
        <text>{{ eventDetail.date }}</text>
      </view>
      <view>
        <text>活动地点: </text>
        <text>{{ eventDetail.location || '暂无信息' }}</text>
      </view>
      <view>
        <text>活动描述: </text>
        <text>{{ eventDetail.description || '暂无信息' }}</text>
      </view>
      <view>
        <text>人数上限: </text>
        <text>{{ eventDetail.capacity || '暂无信息' }}</text>
      </view>
      <view>
        <text>报名状态: </text>
        <text>{{ eventDetail.enrollmentStatus || '暂无信息' }}</text>
      </view>
    </view>
    <view v-else>
      <text>暂无活动详情信息</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      eventDetail: null
    };
  },
  onLoad(options) {
    // 从参数中获取活动的索引
    const index = parseInt(options.index);
    // 根据索引从数据源中获取活动详情
    if (index >= 0) {
      // 假设你使用的是 tableData，你可以根据实际情况调整
      import('../table/tableData.js').then(({ default: tableData }) => {
        this.eventDetail = tableData[index];
      });
    }
  }
};
</script>

<style>
.container {
  padding: 10px;
}
</style>