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
	<!-- 报名按钮 -->
	<button 
	   class="apply-button" 
	   size="mini" 
       type="primary" 
	   @click="applyForEvent"
	>
	    {{ $t('common.button.signin') }}
	</button>
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
        { label: 'Description', field: 'description', icon: 'chat' },
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
  },
  methods: {
      applyForEvent() {
        // 处理报名逻辑
        console.log("用户点击了报名按钮");
        // 这里可以添加调用接口进行报名的代码
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

/* 调整按钮样式 */
.apply-button {
  position: fixed;
  bottom: 30px; /* 稍微上移，避免与底部边界太近 */
  right: 30px;  /* 稍微左移，避免与右侧边界太近 */
  z-index: 999;
  padding: 12px 24px; /* 增大内边距 */
  font-size: 16px;    /* 增大字体 */
  border-radius: 6px; /* 增大圆角 */
}

/* 兼容uni-app的按钮组件样式 */
uni-button.primary {
  background-color: #007aff;
  color: #fff;
  border: none;
}
</style>