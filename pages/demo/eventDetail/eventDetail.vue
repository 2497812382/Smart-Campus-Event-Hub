<template>
  <view class="container">
    <view v-if="eventDetail">
      <view class="detail-item" v-for="(item, index) in detailItems" :key="index">
        <uni-icons :type="item.icon" size="20" color="#999"></uni-icons>
        <text class="item-label">{{ item.label }}</text>
        <text class="item-value">{{ eventDetail[item.field] || '暂无信息' }}</text>
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
      eventDetail: null,
      detailItems: [
        { label: 'Title', field: 'name', icon: 'star' },
        { label: 'Time', field: 'date', icon: 'flag' },
        { label: 'Place', field: 'location', icon: 'location' },
        { label: 'Decription', field: 'description', icon: 'chat' },
        { label: 'Maxmember', field: 'capacity', icon: 'person' },
        { label: 'Enrollment Status', field: 'enrollmentStatus', icon: 'chatbubble' }
      ]
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

<style scoped>
.container {
  padding: 10px;
}

.detail-item {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
}

.item-label {
  margin-left: 10px;
  font-weight: bold;
  color: #333;
}

.item-value {
  margin-left: auto;
  color: #666;
}
</style>