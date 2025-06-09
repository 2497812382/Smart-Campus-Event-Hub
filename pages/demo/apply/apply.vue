<template>
  <view class="apply-page">
    <view class="input-container">
      <!-- 姓名 -->
      <view class="input-label">Name</view>
      <uni-easyinput class="input-box" placeholder="Please enter your name" v-model="formData.name"></uni-easyinput>
      <!-- 邮箱 -->
      <view class="input-label">Email</view>
      <uni-easyinput class="input-box" placeholder="Please enter your email" v-model="formData.email" type="email"></uni-easyinput>
      <!-- 专业 -->
      <view class="input-label">Major</view>
      <uni-easyinput class="input-box" placeholder="Please enter your major" v-model="formData.major"></uni-easyinput>
      <!-- 年级 -->
      <view class="input-label">Grade</view>
      <uni-easyinput class="input-box" placeholder="Please enter your grade" v-model="formData.grade"></uni-easyinput>
      <!-- 特殊偏好 -->
      <view class="input-label">Specific Preferences</view>
      <uni-easyinput class="input-box" placeholder="Please enter your specific preferences" v-model="formData.preferences"></uni-easyinput>
      <!-- 同意照片发布 -->
      <view class="input-label">We may post the photos of the competition on our school website. Do you agree?</view>
      <uni-checkbox-group v-model="formData.agree">
        <uni-checkbox label="Yes"></uni-checkbox>
      </uni-checkbox-group>
    </view>
    <!-- 立即报名按钮 -->
    <button class="apply-now-button" @click="submitApplication">Register now</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        name: '',
        email: '',
        major: '',
        grade: '',
        preferences: '',
        agree: []
      }
    };
  },
  methods: {
    submitApplication() {
      // 这里可以添加提交表单的逻辑，例如调用后端接口
      console.log('提交报名信息:', this.formData);
      // 提交成功后可以跳转到其他页面，例如提示页面
      uni.showToast({
        title: 'success！',
        icon: 'success',
        duration: 2000
      });
      uni.navigateBack(); // 返回上一页
    }
  }
};
</script>

<style scoped>
.apply-page {
  padding: 20px;
}

.input-container {
  margin-bottom: 20px;
}

.input-label {
  font-size: 16px;
  margin-bottom: 5px;
}

.input-box {
  background-color: #f5f5f5;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 15px;
}

.apply-now-button {
  position: fixed;
  bottom: 30px;
  right: 40px;
  background-color: #007aff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>