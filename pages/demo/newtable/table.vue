<template>
	<view>
		<view class="uni-header">
			<view class="uni-group hide-on-phone">
				<view class="uni-title">{{$t('demo.table.title')}}</view>
			</view>
			<view class="uni-group">
				<!-- 输入框 -->
				<input class="uni-search" type="text" v-model="searchVal" @confirm="search" :placeholder="$t('common.placeholder.query')" />
				<!-- 搜索按钮 -->
				<button class="uni-button" type="default" size="mini" @click="search">{{$t('common.button.search')}}</button>
			</view>
		</view>
		<view class="uni-container">
			<!-- 表格组件 1-->
			<uni-table :loading="loading" border stripe type="selection" :emptyText="$t('common.empty')" @selection-change="selectionChange">
				<uni-tr>
					<!-- 表头列 -->
					<uni-th width="150" align="center">date</uni-th>
					<uni-th width="150" align="center">classification</uni-th>
					<uni-th align="center">name</uni-th>
					<uni-th width="150" align="center">popularity</uni-th>
					<uni-th width="204" align="center">operation</uni-th>
				</uni-tr>
				<uni-tr v-for="(item ,index) in tableData" :key="index">
					<!-- 表格数据列 -->
					<uni-td style="text-align: center; vertical-align: middle;">{{item.date}}</uni-td>
					<uni-td style="text-align: center; vertical-align: middle;">
						<view class="name">{{item.classification}}</view>
					</uni-td>
					<uni-td style="text-align: center; vertical-align: middle;">{{item.name}}</uni-td>
					<uni-td style="text-align: center; vertical-align: middle;">{{item.popularity}}</uni-td> <!-- 新增列的数据，可根据实际情况修 -->
					<uni-td>
						<view class="uni-group">
							
							<!-- 签到按钮 -->
							<button class="uni-button" size="mini" type="primary">{{$t('common.button.signup')}}</button>
						</view>
					</uni-td>
				</uni-tr>
			</uni-table>
			<view class="uni-pagination-box">
				<!-- 分页组件 -->
				<uni-pagination show-icon :page-size="pageSize" :current="pageCurrent" :total="total" @change="change" />
			</view>
		</view>
		<!-- #ifndef H5 -->
		<fix-window />
		<!-- #endif -->
	</view>
</template>


<script>
	// 导入名为 "tableData" 的模块，路径为 './tableData.js'
	import tableData from './newtableData.js'

	// 导出默认模块
	export default {
		name: 'NewTablePage', // 修改组件名称
		// 数据属性
		data() {
			return {
				// 搜索值
				searchVal: '',
				// 表格数据
				tableData: [],
				// 每页数据量
				pageSize: 10,
				// 当前页
				pageCurrent: 1,
				// 数据总量
				total: 0,
				// 加载状态
				loading: false
			}
		},

		// 页面加载时的处理函数
		onLoad() {
			// 重置选中项数组
			this.selectedIndexs = []
			// 获取第一页数据
			this.getData(1)
		},

		// 方法
		methods: {
			// 多选处理
			selectedItems() {
				return this.selectedIndexs.map(i => this.tableData[i])
			},

			// 多选事件处理函数
			selectionChange(e) {
				this.selectedIndexs = e.detail.index
			},

			// 批量删除函数
			delTable() {
				this.selectedItems();
			},

			// 分页触发事件处理函数
			change(e) {
				this.getData(e.current)
			},

			// 搜索函数
			search() {
				this.getData(1, this.searchVal)
			},

			// 获取数据函数
			getData(pageCurrent, value = "") {
				this.loading = true
				this.pageCurrent = pageCurrent
				this.request({
					pageSize: this.pageSize,
					pageCurrent: pageCurrent,
					value: value,
					success: (res) => {
						this.tableData = res.data
						this.total = res.total
						this.loading = false
					}
				})
			},

			// 伪request请求函数
			request(options) {
				const {
					pageSize,
					pageCurrent,
					success,
					value
				} = options

				let total = tableData.length

				let data = tableData.filter((item, index) => {
					const idx = index - (pageCurrent - 1) * pageSize
					return idx < pageSize && idx >= 0
				})

				if (value) {
					data = []
					tableData.forEach(item => {
						if (item.name.indexOf(value) !== -1) {
							data.push(item)
						}
					})
					total = data.length
				}

				setTimeout(() => {
					typeof success === 'function' && success({
						data: data,
						total: total
					})
				}, 500)
			}
		}
	}
</script>


<style>
	/* #ifndef H5 */
	page {
		padding-top: 85px;
	}

	/* #endif */
</style>
