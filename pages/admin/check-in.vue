<template>
  <view class="checkin-monitor-page">
    <!-- 页面标题 -->
    <view class="page-title">check-in monitor</view>

    <!-- 搜索和筛选区域 -->
    <view class="filter-container">
      <uni-search-bar v-model="searchKeyword" @confirm="searchEvents" placeholder="Search"></uni-search-bar>
      <view class="filter-options">
        <uni-datetime-picker v-model="selectedDate" type="date" placeholder="Date"></uni-datetime-picker>
        <uni-select v-model="selectedStatus" :options="statusOptions" placeholder="Status"></uni-select>
        <button class="search-btn" @click="searchEvents">Search</button>
      </view>
    </view>

    <!-- 主表格：事件列表 -->
    <view class="main-table-container">
      <uni-table :data="eventList" :columns="mainColumns" border stripe>
        <template #cell(eventName)="scope">
          <text class="event-name">{{ scope.row.eventName }}</text>
        </template>
        <template #cell(checkinCount)="scope">
          <text class="checkin-count">{{ scope.row.checkinCount }}/{{ scope.row.totalStudents }}</text>
        </template>
        <template #cell(actions)="scope">
          <button 
            class="detail-btn" 
            :class="{ 'active': scope.row.showDetail }"
            @click="toggleDetail(scope.row.eventId)">
            {{ scope.row.showDetail ? 'Detail' : 'Detail' }}
          </button>
          <button 
            class="lock-btn" 
            :disabled="scope.row.locked"
            @click="lockEvent(scope.row.eventId)">
            {{ scope.row.locked ? 'Locked' : 'Lock' }}
          </button>
        </template>
      </uni-table>
    </view>

    <!-- 副表格：学生签到详情 (动态显示) -->
    <view v-for="(event, index) in eventList" :key="event.eventId" class="sub-table-container" v-show="event.showDetail">
      <view class="sub-table-title">
        {{ event.eventName }} - check-in details
      </view>
      <uni-table :data="event.studentList" :columns="subColumns" border stripe>
        <template #cell(studentName)="scope">
          <text>{{ scope.row.studentName }}</text>
        </template>
        <template #cell(grade)="scope">
          <text>{{ scope.row.grade }}</text>
        </template>
        <template #cell(major)="scope">
          <text>{{ scope.row.major }}</text>
        </template>
        <template #cell(checkinTime)="scope">
          <text class="checkin-time">{{ scope.row.checkinTime || 'no check-in' }}</text>
        </template>
        <template #cell(actions)="scope">
          <button 
            class="edit-btn" 
            :disabled="event.locked"
            @click="editCheckinStatus(event.eventId, scope.row.studentId)">
            Edit
          </button>
        </template>
      </uni-table>
    </view>

    <!-- 编辑签到状态弹窗 -->
    <uni-popup ref="editPopup" type="center">
      <view class="popup-content">
        <view class="popup-title">编辑签到状态</view>
        <view class="form-item">
          <text class="label">Name:</text>
          <text class="value">{{ currentEditStudent.studentName || '-' }}</text>
        </view>
        <view class="form-item">
          <text class="label">签到状态：</text>
          <uni-radio-group v-model="currentEditStatus">
            <uni-radio label="Checked in" value="checked"></uni-radio>
            <uni-radio label="No check-in" value="unchecked"></uni-radio>
          </uni-radio-group>
        </view>
        <view class="form-item">
          <text class="label">Time：</text>
          <uni-datetime-picker v-model="currentEditTime" type="datetime"></uni-datetime-picker>
        </view>
        <view class="popup-buttons">
          <button class="cancel-btn" @click="closeEditPopup">Cancel</button>
          <button class="confirm-btn" @click="saveCheckinStatus">Confirm</button>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 搜索和筛选相关
      searchKeyword: '',
      selectedDate: '',
      selectedStatus: '',
      statusOptions: [
        { text: 'All', value: '' },
        { text: 'Active', value: 'active' },
        { text: 'Ended', value: 'ended' },
        { text: 'Locked', value: 'locked' }
      ],
      
      // 主表格数据
      eventList: [],
      mainColumns: [
        { title: 'Name', key: 'eventName', align: 'center' },
        { title: 'Count', key: 'checkinCount', align: 'center' },
        { title: 'Operation', key: 'actions', align: 'center' }
      ],
      
      // 副表格数据
      subColumns: [
        { title: 'Name', key: 'studentName', align: 'center' },
        { title: 'Grade', key: 'grade', align: 'center' },
        { title: 'Major', key: 'major', align: 'center' },
        { title: 'Time', key: 'checkinTime', align: 'center' },
        { title: 'Operation', key: 'actions', align: 'center' }
      ],
      
      // 编辑弹窗相关
      currentEditEventId: '',
      currentEditStudentId: '',
      currentEditStudent: {},
      currentEditStatus: 'checked',
      currentEditTime: '',
      
      // 分页相关
      currentPage: 1,
      pageSize: 10,
      totalEvents: 0
    };
  },
  methods: {
    // 获取事件列表
    async fetchEventList() {
      try {
        const res = await uniCloud.callFunction({
          name: 'getEventList',
          data: {
            keyword: this.searchKeyword,
            date: this.selectedDate,
            status: this.selectedStatus,
            page: this.currentPage,
            pageSize: this.pageSize
          }
        });
        
        if (res.result.code === 0) {
          this.eventList = res.result.data.map(event => ({
            ...event,
            showDetail: false // 控制详情是否展开
          }));
          this.totalEvents = res.result.total;
        } else {
          uni.showToast({
            title: 'Failed to get event list.',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('Failed to get event list.', error);
        uni.showToast({
          title: 'Network error, please try again.',
          icon: 'none'
        });
      }
    },
    
    // 切换事件详情显示/隐藏
    toggleDetail(eventId) {
      const event = this.eventList.find(item => item.eventId === eventId);
      if (event) {
        if (!event.showDetail) {
          // 如果详情未展开，则加载学生列表
          this.loadStudentList(eventId);
        }
        event.showDetail = !event.showDetail;
      }
    },
    
    // 加载学生列表
    async loadStudentList(eventId) {
      try {
        const res = await uniCloud.callFunction({
          name: 'getStudentListByEvent',
          data: { eventId }
        });
        
        if (res.result.code === 0) {
          const eventIndex = this.eventList.findIndex(item => item.eventId === eventId);
          if (eventIndex !== -1) {
            this.eventList[eventIndex].studentList = res.result.data;
          }
        } else {
          uni.showToast({
            title: 'Failed to get student list.',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('Failed to get student list.', error);
        uni.showToast({
          title: 'Network error, please try again.',
          icon: 'none'
        });
      }
    },
    
    // 锁定事件
    async lockEvent(eventId) {
      const confirmResult = await uni.showModal({
        title: 'Confirm lock',
        content: 'After locking, you will not be able to modify the sign-in status of this event. Continue?',
        confirmText: 'Confirm',
        cancelText: 'Cancel'
      });
      
      if (confirmResult.confirm) {
        try {
          const res = await uniCloud.callFunction({
            name: 'lockEvent',
            data: { eventId }
          });
          
          if (res.result.code === 0) {
            const eventIndex = this.eventList.findIndex(item => item.eventId === eventId);
            if (eventIndex !== -1) {
              this.eventList[eventIndex].locked = true;
            }
            uni.showToast({
              title: 'Lock success',
              icon: 'success'
            });
          } else {
            uni.showToast({
              title: 'Lock failed',
              icon: 'none'
            });
          }
        } catch (error) {
          console.error('Lock failed', error);
          uni.showToast({
            title: 'Network error, please try again.',
            icon: 'none'
          });
        }
      }
    },
    
    // 打开编辑签到状态弹窗
    editCheckinStatus(eventId, studentId) {
      const event = this.eventList.find(item => item.eventId === eventId);
      if (!event || event.locked) return;
      
      const student = event.studentList.find(item => item.studentId === studentId);
      if (student) {
        this.currentEditEventId = eventId;
        this.currentEditStudentId = studentId;
        this.currentEditStudent = student;
        
        // 设置初始值
        if (student.checkinTime) {
          this.currentEditStatus = student.status || 'checked';
          this.currentEditTime = student.checkinTime;
        } else {
          this.currentEditStatus = 'unchecked';
          this.currentEditTime = '';
        }
        
        // 显示弹窗
        this.$refs.editPopup.open();
      }
    },
    
    // 关闭编辑弹窗
    closeEditPopup() {
      this.$refs.editPopup.close();
    },
    
    // 保存签到状态
    async saveCheckinStatus() {
      try {
        const res = await uniCloud.callFunction({
          name: 'updateCheckinStatus',
          data: {
            eventId: this.currentEditEventId,
            studentId: this.currentEditStudentId,
            status: this.currentEditStatus,
            checkinTime: this.currentEditStatus === 'checked' || this.currentEditStatus === 'late' 
              ? this.currentEditTime 
              : null
          }
        });
        
        if (res.result.code === 0) {
          // 更新本地数据
          const eventIndex = this.eventList.findIndex(item => item.eventId === this.currentEditEventId);
          if (eventIndex !== -1) {
            const studentIndex = this.eventList[eventIndex].studentList.findIndex(
              item => item.studentId === this.currentEditStudentId
            );
            if (studentIndex !== -1) {
              this.eventList[eventIndex].studentList[studentIndex].status = this.currentEditStatus;
              this.eventList[eventIndex].studentList[studentIndex].checkinTime = 
                this.currentEditStatus === 'checked' || this.currentEditStatus === 'late' 
                  ? this.currentEditTime 
                  : null;
              
              // 更新签到统计
              this.updateCheckinCount(eventIndex);
            }
          }
          
          uni.showToast({
            title: 'Edit success',
            icon: 'success'
          });
          this.closeEditPopup();
        } else {
          uni.showToast({
            title: 'Edit failed',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('Edit failed', error);
        uni.showToast({
          title: 'Network error, please try again.',
          icon: 'none'
        });
      }
    },
    
    // 更新签到统计
    updateCheckinCount(eventIndex) {
      const studentList = this.eventList[eventIndex].studentList;
      const checkedInCount = studentList.filter(student => 
        student.status === 'checked' || student.status === 'late'
      ).length;
      
      this.eventList[eventIndex].checkinCount = checkedInCount;
    },
    
    // 搜索事件
    searchEvents() {
      this.currentPage = 1;
      this.fetchEventList();
    },
    
    // 分页变化
    onPageChange(page) {
      this.currentPage = page;
      this.fetchEventList();
    }
  },
  onLoad() {
    this.fetchEventList();
  }
};
</script>

<style scoped>
.page-title {
  font-size: 36rpx;
  font-weight: bold;
  padding: 30rpx 20rpx;
  text-align: center;
}

.filter-container {
  padding: 0 20rpx 20rpx;
}

.filter-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20rpx;
}

.search-btn {
  background-color: #1677ff;
  color: white;
  padding: 10rpx 30rpx;
  border-radius: 8rpx;
}

.main-table-container {
  padding: 0 20rpx;
}

.sub-table-container {
  padding: 20rpx;
  background-color: #f5f7fa;
  margin-bottom: 20rpx;
}

.sub-table-title {
  font-size: 28rpx;
  font-weight: bold;
  margin-bottom: 15rpx;
}

.event-name {
  font-weight: bold;
}

.checkin-count {
  color: #1677ff;
}

.checkin-time {
  color: #00b42a;
}

.detail-btn {
  background-color: #1677ff;
  color: white;
  border-radius: 6rpx;
  padding: 8rpx 15rpx;
  margin-right: 10rpx;
}

.detail-btn.active {
  background-color: #00b42a;
}

.lock-btn {
  background-color: #ff4d4f;
  color: white;
  border-radius: 6rpx;
  padding: 8rpx 15rpx;
}

.lock-btn[disabled] {
  background-color: #d9d9d9;
  cursor: not-allowed;
}

.edit-btn {
  background-color: #00b42a;
  color: white;
  border-radius: 6rpx;
  padding: 8rpx 15rpx;
}

.edit-btn[disabled] {
  background-color: #d9d9d9;
  cursor: not-allowed;
}

/* 弹窗样式 */
.popup-content {
  width: 600rpx;
  background-color: white;
  border-radius: 16rpx;
  padding: 30rpx;
}

.popup-title {
  font-size: 32rpx;
  font-weight: bold;
  text-align: center;
  margin-bottom: 30rpx;
}

.form-item {
  margin-bottom: 25rpx;
}

.label {
  display: inline-block;
  width: 180rpx;
  font-size: 28rpx;
}

.value {
  font-size: 28rpx;
}

.popup-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 40rpx;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  padding: 15rpx 60rpx;
  border-radius: 10rpx;
}

.confirm-btn {
  background-color: #1677ff;
  color: white;
  padding: 15rpx 60rpx;
  border-radius: 10rpx;
}
</style>