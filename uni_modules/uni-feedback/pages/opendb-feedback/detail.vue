<template>
  <view class="container">
    <unicloud-db ref="udb" v-slot:default="{data, loading, error, options}" :options="options" collection="opendb-feedback" field="content,imgs,contact,mobile" :where="queryWhere" :getone="true" :manual="true">
      <view v-if="error">{{error.message}}</view>
      <view v-else-if="loading">
        <uni-load-more :contentText="loadMore" status="loading"></uni-load-more>
      </view>
      <view v-else-if="data">
        <view>
          <text>留言内容/回复内容</text>
          <text>{{data.content}}</text>
        </view>
        <view>
          <text>图片列表</text>
          <template v-for="(file, j) in data.imgs">
            <uni-file-picker v-if="file.fileType == 'image'" :value="file" :file-mediatype="file.fileType" return-type="object" readonly></uni-file-picker>
            <uni-link v-else :href="file.url" :text="file.url"></uni-link>
          </template>
        </view>
        <view>
          <text>联系人</text>
          <text>{{data.contact}}</text>
        </view>
        <view>
          <text>联系电话</text>
          <text>{{data.mobile}}</text>
        </view>
      </view>
    </unicloud-db>
    <view class="btns">
      <button type="primary" @click="handleUpdate">修改</button>
	  <button type="primary" @click="showEventDetail">详情</button>
      <button type="warn" class="btn-delete" @click="handleDelete">删除</button>
    </view>
  </view>
</template>

<script>
  // 由schema2code生成，包含校验规则和enum静态数据
  import { enumConverter } from '../../js_sdk/validator/opendb-feedback.js';

  export default {
    data() {
      return {
        queryWhere: '',
		eventDetail: null, // 用于存储活动详细信息
        loadMore: {
          contentdown: '',
          contentrefresh: '',
          contentnomore: ''
        },
        options: {
          // 将scheme enum 属性静态数据中的value转成text
          ...enumConverter
        }
      }
    },
    onLoad(e) {
      this._id = e.id
    },
    onReady() {
      if (this._id) {
        this.queryWhere = '_id=="' + this._id + '"'
      }
    },
    methods: {
      handleUpdate() {
        // 打开修改页面
        uni.navigateTo({
          url: './edit?id=' + this._id,
          events: {
            // 监听修改页面成功修改数据后, 刷新当前页面数据
            refreshData: () => {
              this.$refs.udb.loadData({
                clear: true
              })
            }
          }
        })
      },
	  showEventDetail() {
	        // 调用获取活动详情的方法
	        this.getEventDetail();
	      },
	      async getEventDetail() {
	        try {
	          // 假设这里调用后端接口获取活动详情
	          const res = await uniCloud.callFunction({
	            name: 'getEventDetail', // 后端云函数名称
	            data: {
	              eventId: this.id // 假设这里有活动的 ID
	            }
	          });
	          this.eventDetail = res.result.data;
	          // 显示弹出窗口
	          this.showDetailPopup();
	        } catch (err) {
	          uni.showModal({
	            content: err.message || '请求服务失败',
	            showCancel: false
	          });
	        }
	      },
	      showDetailPopup() {
	        // 这里可以使用 uni-popup 或其他弹窗组件显示详情
	        // 示例代码，假设使用 uni-popup
	        this.$refs.detailPopup.open();
	      },
      handleDelete() {
        this.$refs.udb.remove(this._id, {
          success: (res) => {
            // 删除数据成功后跳转到list页面
            uni.navigateTo({
              url: './list'
            })
          }
        })
      }
    }
  }
</script>

<style>
  .container {
    padding: 10px;
  }

  .btns {
    margin-top: 10px;
    /* #ifndef APP-NVUE */
    display: flex;
    /* #endif */
    flex-direction: row;
  }

  .btns button {
    flex: 1;
  }

  .btn-delete {
    margin-left: 10px;
  }
</style>
