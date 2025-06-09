<template>
  <view class="event-management-page">
    <!-- 页面标题 -->
    <view class="page-title">Event Management</view>

    <!-- 添加活动表单 -->
    <uni-forms ref="addEventForm" :modelValue="addEventData">
      <uni-forms-item label="Name">
        <uni-input v-model="addEventData.name"></uni-input>
      </uni-forms-item>
      <uni-forms-item label="Time">
        <uni-datetime-picker v-model="addEventData.time" type="datetime"></uni-datetime-picker>
      </uni-forms-item>
      <uni-forms-item label="Description">
        <uni-input v-model="addEventData.description"></uni-input>
      </uni-forms-item>
      <uni-forms-item label="Location">
        <uni-input v-model="addEventData.location"></uni-input>
      </uni-forms-item>
      <button class="button1"@click="submitAddEvent">creat event</button>
    </uni-forms>

    <!-- 活动列表 -->
    <uni-table :data="events" :columns="columns">
      <template #cell(name)="scope">
        {{ scope.row.name }}
      </template>
      <template #cell(time)="scope">
        {{ scope.row.time }}
      </template>
      <template #cell(description)="scope">
        {{ scope.row.description }}
      </template>
      <template #cell(location)="scope">
        {{ scope.row.location }}
      </template>
      <template #cell(status)="scope">
        {{ getStatusText(scope.row.status) }}
      </template>
      <template #cell(actions)="scope">
        <button class="button2"@click="editEvent(scope.row.id)" :disabled="scope.row.status!== 'Normal'">Edit</button>
        <button class="button3"@click="cancelEvent(scope.row.id)" :disabled="scope.row.status!== 'Normal'">Cancel</button>
        <button class="button4"@click="closeEvent(scope.row.id)" :disabled="scope.row.status!== 'Normal'">Close</button>
      </template>
    </uni-table>

    <!-- 分页组件 -->
    <uni-pagination
      :total="totalEvents"
      :page-size="pageSize"
      :current-page="currentPage"
      @change="onPageChange"
    ></uni-pagination>
  </view>
</template>

<script>
export default {
  data() {
    return {
      addEventData: {
        name: '',
        time: '',
        description: '',
        location: '',
        status: 'Normal'
      },
      events: [],
      columns: [
        { title: 'Name', key: 'name' },
        { title: 'Time', key: 'time' },
        { title: 'Description', key: 'description' },
        { title: 'Location', key: 'location' },
        { title: 'Status', key: 'status' },
        { title: 'Operation', key: 'actions' }
      ],
      totalEvents: 0,
      pageSize: 10,
      currentPage: 1
    };
  },
  methods: {
    // 添加活动
    async submitAddEvent() {
      try {
        const res = await uniCloud.callFunction({
          name: 'add-event',
          data: this.addEventData
        });
        if (res.result.code === 0) {
          uni.showToast({
            title: 'create event success',
            icon: 'success'
          });
          this.addEventData = {
            name: '',
            time: '',
            description: '',
            location: '',
            status: 'Normal'
          };
          this.getEvents();
        } else {
          uni.showToast({
            title: 'create event failed',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('create event failed', error);
        uni.showToast({
          title: 'create event failed',
          icon: 'none'
        });
      }
    },
    // 获取活动列表
    async getEvents() {
      try {
        const res = await uniCloud.callFunction({
          name: 'get-events',
          data: {
            page: this.currentPage,
            pageSize: this.pageSize
          }
        });
        this.events = res.result.data;
        this.totalEvents = res.result.total;
      } catch (error) {
        console.error('Failed to get event list.:', error);
      }
    },
    // 编辑活动
    async editEvent(id) {
      const event = this.events.find(item => item.id === id);
      if (event) {
        const { name, time, description, location } = await uni.showModal({
          title: 'Edit',
          editable: true,
          content: `Name:${event.name}\nTime:${event.time}\nDescription:${event.description}\nLocation:${event.location}`,
          placeholderText: 'Please enter new activity information, one message per line, in the order of name, time, description and place.',
          confirmText: 'Save',
          cancelText: 'Cancel'
        });
        if (name) {
          const [newName, newTime, newDescription, newLocation] = name.split('\n');
          const updatedEvent = {
            id,
            name: newName || event.name,
            time: newTime || event.time,
            description: newDescription || event.description,
            location: newLocation || event.location
          };
          try {
            const res = await uniCloud.callFunction({
              name: 'update-event',
              data: updatedEvent
            });
            if (res.result.code === 0) {
              uni.showToast({
                title: 'Edit event success',
                icon: 'success'
              });
              this.getEvents();
            } else {
              uni.showToast({
                title: 'Edit event failed',
                icon: 'none'
              });
            }
          } catch (error) {
            console.error('Edit event failed', error);
            uni.showToast({
              title: 'Edit event failed',
              icon: 'none'
            });
          }
        }
      }
    },
    // 取消活动
    async cancelEvent(id) {
      try {
        const res = await uniCloud.callFunction({
          name: 'update-event-status',
          data: {
            id,
            status: 'Canceled'
          }
        });
        if (res.result.code === 0) {
          uni.showToast({
            title: 'Cancel event success',
            icon: 'success'
          });
          this.getEvents();
        } else {
          uni.showToast({
            title: 'Cancel event failed',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('Cancel event failed', error);
        uni.showToast({
          title: 'Cancel event failed',
          icon: 'none'
        });
      }
    },
    // 关闭活动
    async closeEvent(id) {
      try {
        const res = await uniCloud.callFunction({
          name: 'update-event-status',
          data: {
            id,
            status: 'Closed'
          }
        });
        if (res.result.code === 0) {
          uni.showToast({
            title: 'Close event success',
            icon: 'success'
          });
          this.getEvents();
        } else {
          uni.showToast({
            title: 'Close event failed',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('Close event failed', error);
        uni.showToast({
          title: 'Close event failed',
          icon: 'none'
        });
      }
    },
    // 分页变化
    onPageChange(page) {
      this.currentPage = page;
      this.getEvents();
    },
    // 获取状态文本
    getStatusText(status) {
      switch (status) {
        case 'Normal':
          return 'Normal';
        case 'Canceled':
          return 'Canceled';
        case 'Closed':
          return 'Closed';
        default:
          return 'Unknown';
      }
    }
  },
  created() {
    this.getEvents();
  }
};
</script>

<style scoped>
.event-management-page {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

uni-forms {
  margin-bottom: 20px;
}

uni-table {
  margin-bottom: 20px;
}
.button1{
  position: fixed;
  bottom: 30px;
  right: 40px;
  background-color: #2a82e4;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.button2{
  position: fixed;
  bottom: 30px;
  right: 40px;
  background-color: #43cf7c;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.button3{
  position: fixed;
  bottom: 30px;
  right: 40px;
  background-color: #d43030;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.button4{
  position: fixed;
  bottom: 30px;
  right: 40px;
  background-color: #ff8d1a;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>