<template>
  <div>
    <!-- 查询内容、重置按钮 -->
    <div>
      <el-form
        :inline="true"
        :model="formInline"
        ref="formInline"
        class="demo-form-inline searchStyle"
      >
        <el-form-item label="账号:" prop="customerNumber">
          <el-input v-model="formInline.customerNumber" clearable></el-input>
        </el-form-item>
        <el-form-item label="用户姓名:" prop="customerName">
          <el-input v-model="formInline.customerName" clearable></el-input>
        </el-form-item>
        <el-form-item label="性别:" prop="userGender">
          <el-select v-model="formInline.userGender" clearable placeholder="请选择">
            <el-option
              v-for="item in optionsUserGender"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchForm()">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="resetForm('formInline')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!-- 新增修改按钮 -->
    <div class="handle-box">
      <el-button type="primary" icon="el-icon-setting" @click="addAccount('addInfo')">新增</el-button>
      <el-button type="primary" icon="el-icon-setting" @click="editAccount()">修改</el-button>
      <el-button type="primary" icon="el-icon-setting" @click="EnableAccount()">启用</el-button>
      <el-button type="primary" icon="el-icon-setting" @click="DisEnableAccount()">禁用</el-button>
    </div>
    <!-- 显示内容的表格，内容由tableData显示 -->
    <el-table
      :data="tableData"
      border
      stripe
      @select="chooseOne"
      @select-all="chooseAll"
      style="width: 100%">
      <el-table-column type="selection" width="55" align="center"></el-table-column>
      <el-table-column prop="customerNumber" label="账号" width="180"></el-table-column>
      <el-table-column prop="customerName" label="用户名" width="180"></el-table-column>
      <el-table-column label="启用/禁用">
        <template slot-scope="scope">
          <span v-if="1 == scope.row.customerIsUsed">启用</span>
          <span v-else-if="0 == scope.row.customerIsUsed">禁用</span>
          <span v-else>不详</span>
        </template>
      </el-table-column>
    </el-table>
    <!-- element分页组件 -->
    <div class="pagination">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pageNum"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="dataSize"
      ></el-pagination>
    </div>
    <!-- 新增账号的dialog -->
    <el-dialog
      width="52%"
      title="新增账号"
      :visible.sync="dialogAdd"
      :close-on-click-modal="false"
      class="accoutDialog">
      <el-form
        :model="addInfo"
        label-width="200px"
        :rules="rules"
        ref="addInfo"
        :inline="true"
        :label-position="'right'"
      >
        <!-- <el-form  label-width="100px" :inline="true" :label-position="'right'"> -->
        <el-form-item label="账号" prop="customerNumber">
          <el-input v-model="addInfo.customerNumber" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="customerName">
          <el-input v-model="addInfo.customerName" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="passWord">
          <el-input type="password" v-model="addInfo.customePassword" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="passWordCheck">
          <el-input type="password" v-model="addInfo.passWordCheck" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="customerIsUsed">
          <el-select v-model="addInfo.customerIsUsed" class="inputWidth">
            <el-option label="启用" value="1" style="padding-right:0px !important"></el-option>
            <el-option label="禁用" value="0" style="padding-right:0px !important"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">取 消</el-button>
        <el-button type="primary" @click="addSure('addInfo')">确 定</el-button>
      </div>
    </el-dialog>
    <!-- 修改账号的dialog -->  
    <el-dialog
      width="52%"
      title="修改账号"
      :visible.sync="dialogEdit"
      :close-on-click-modal="false"
      class="accoutDialog"
      :before-close="cancelDialog">
      <el-form
        :model="editInfo"
        label-width="200px"
        :rules="rules"
        ref="editInfo"
        :inline="true"
        :label-position="'right'"
      >
        <el-form-item label="用户名" prop="customerName">
          <el-input v-model="editInfo.customerName" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="customerIsUsed">
          <el-select v-model="editInfo.customerIsUsed" class="inputWidth">
            <el-option label="启用" value="1" style="padding-right:0px !important"></el-option>
            <el-option label="禁用" value="0" style="padding-right:0px !important"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">取 消</el-button>
        <el-button type="primary" @click="editSure('editInfo')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
export default {
  data() {
    //表单验证飞控去空格后非空
    var validatePass = (rule, value, callback) => {
      if (value.replace(/(^\s*)|(\s*$)/g, "") === '') {//前后去空格
        callback(new Error('请输入用户名称'));
      } else {
        callback();
      }
    };
    //修改
    var validatePass2 = (rule, value, callback) => {
      if (value.replace(/(^\s*)|(\s*$)/g, "") === '') {//前后去空格
        callback(new Error('请输入用户账号'));
      } else {
        callback();
      }
    };
    //密码
    var validatePassWord = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        if (this.addInfo.passWordCheck !== '') {
          this.$refs.addInfo.validateField('passWordCheck');
        }
        callback();
      }
    };
    //密码确认
    var validatePassWordCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.addInfo.customePassword) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      loading: '',//加载遮罩
      selectId: [],//选中的id
      dialogAdd: false,//新增框默认隐藏
      dialogEdit: false,//修改框默认隐藏
      addUrl: this.$store.state.url + 'customerManager/backend/customer/addCustomer',//新增
      editUrl: this.$store.state.url + 'customerManager/backend/customer/updateAccount',//修改           
      getDataUrl:this.$store.state.url + 'customerManager/backend/customer/getCustomerList',
      getCustomerDetailUrl: this.$store.state.url + 'customerManager/backend/customer/getCustomerDetail',//修改获取用户信息
      IsUsedUrl: this.$store.state.url + 'customerManager/backend/customer/updateAccountByStatus',//修改状态
      formInline: {//快捷查询
        customerName: '',
        customerNumber: '',
        userGender: ''
      },
      optionsUserGender: [
        {
          value: '1',
          label: '男'
        },
        {
          value: '0',
          label: '女'
        }
      ],
      rules: {//表单验证
        customerNumber: [
          { required: true, validator: validatePass2, trigger: 'blur' },// //,
          { min: 1, max: 40, message: '长度在 1 到 40 个字符', trigger: 'blur' }
        ],
        customerName: [
          { required: true, validator: validatePass, trigger: 'blur' },
          { min: 1, max: 40, message: '长度在 1 到 40 个字符', trigger: 'blur' }
        ],
        customePassword: [
          { required: true, validator: validatePassWord, trigger: 'blur' }
        ],
        passWordCheck: [
          { required: true, validator: validatePassWordCheck, trigger: 'blur' }
        ],
      },
      tableData: [
          {
            customerId:'1',
            customerNumber:'测试',//角色code
            customerName:'测试',//角色code
            customerIsUsed:'0'
          },
          {
            customerId:'2',
            customerNumber:'测试',//角色code
            customerName:'测试',//角色code
            customerIsUsed:'1'
          },
          {
            customerId:'3',
            customerNumber:'测试',//角色code
            customerName:'测试',//角色code
            customerIsUsed:'1'
          },
          {
            customerId:'4',
            customerNumber:'测试',//角色code
            customerName:'测试',//角色code
            customerIsUsed:'1'
          },
          {
            customerId:'5',
            customerNumber:'测试',//角色code
            customerName:'测试',//角色code
            customerIsUsed:'1'
          },
      ],
      addInfo: {
        customerNumber: '',//用户登陆账号
        customerName: '',
        customerIsUsed: '1',//0禁用1启用
        customePassword: '',
        passWordCheck: '',
      },
      pageNum: 1,
      pageSize: 10,
      dataSize: 5,

      editInfo: {},//待修改的参数
      editInfoBefore: '',//修改前的值 取消修改用
    }
  },
  // 监听分页
  watch: {
    pageNum: function () {
      this.getData();
    },
    pageSize: function () {
      this.getData();
    },
  },
  mounted: function () {
      // 页面开启的数据获取
    this.$nextTick(function () {
      this.getData();
    })
  },
  methods: {
    // 打开加载
    openFullScreen() {
      this.loading = this.$loading({
        lock: true,
        text: '操作中...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
    },
    //获取页面按钮
    chooseClick(method) {
      if ('addAccount' == method) {
        this.addAccount('addInfo');
      } else if ('editAccount' == method) {
        this.editAccount();
      } else if ('EnableAccount' == method) {
        this.EnableAccount();
      } else if ('DisEnableAccount' == method) {
        this.DisEnableAccount();
      }
    },
    // 新增账号，显示dialog
    addAccount(addInfo) {
      this.dialogAdd = true;
      if (this.$refs[addInfo]) {//清空表单
        this.$refs[addInfo].resetFields();
      }
    },
    // 获取数据，请求服务器存到tableData
    getData() {
      this.openFullScreen();//打开遮罩
      var params = {
        'customerName': this.formInline.customerName,
        'customerNumber': this.formInline.customerNumber,
        'customerIsUsed': this.formInline.customerIsUsed
      };
      this.$axios.get(this.getDataUrl + '?pageSize=' + this.pageSize + '&pageNum=' + this.pageNum, params).then(res => {
        this.loading.close(); //关闭加载
        this.editInfoBefore = {};
        this.selectId = {};
        if (0 == res.data.code) {
          this.tableData = res.data.data.list;
          this.dataSize = res.data.data.totalRecords;
        } else {
          this.$message({
            showClose: true,
            message: res.data.msg,
            type: 'error'
          });
        }
      });
    },
    // 查询
    searchForm() {
      var params = new URLSearchParams();
      params.append('customerNumber', this.formInline.customerNumber);
      params.append('customerIsUsed', this.formInline.customerIsUsed);
      params.append('customerName', this.formInline.customerName);
      params.append('pageNum', this.pageNum);
      params.append('pageSize', this.pageSize);
      this.formData = params;
      if (1 != this.pageNum) {
        this.pageNum = 1;//每次查询从第一页开始
      } else {
        this.getData();
      }
    },
    // 重置按钮
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    //确认新增
    addSure(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var params = new URLSearchParams();
          params.append('customerNumber', this.addInfo.customerNumber);
          params.append('customerName', this.addInfo.customerName);
          params.append('customerIsUsed', this.addInfo.customerIsUsed);
          params.append('customePassword', this.addInfo.customePassword);
          this.openFullScreen();//打开遮罩
          this.$axios.post(this.addUrl, params).then(res => {
            this.loading.close(); //关闭加载
            if (0 == res.data.code) {//新增成功
              this.getData();
              this.$message({
                showClose: true,
                message: '新增账号成功',
                type: 'success'
              });
              this.dialogAdd = false;//隐藏dialo  
            } else {
              this.$message({
                showClose: true,
                message: res.data.msg,
                type: 'error'
              });
            }
          });
        }else {
          return false;
        }
      });
    },
    // 修改（编辑）账号
    editAccount(form) {
      if (this.editInfoBefore) {
        if (1 == this.selectId.length) {
          this.dialogEdit = true;
          this.editInfo = JSON.parse(JSON.stringify(this.editInfoBefore))
        } else {
          this.$message({
            showClose: true,
            message: "请选择一条数据进行修改",
            type: 'error'
          });
        }
      } else {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行修改",
          type: 'error'
        });
      }
    },
    //确认修改
    editSure(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var params = new URLSearchParams();
          params.append('customerId', this.editInfo.customerId);
          params.append('customerName', this.editInfo.customerName);
          params.append('customerIsUsed', this.editInfo.customerIsUsed);
          this.openFullScreen();//打开遮罩
          this.$axios.put(this.editUrl, params).then(res => {
            this.loading.close(); //关闭加载
            if (0 == res.data.code) {//修改成功
              this.getData();
              this.$message({
                showClose: true,
                message: '修改用户成功',
                type: 'success'
              });
              this.dialogEdit = false;//隐藏dialo 
            } else {
              this.$message({
                showClose: true,
                message: res.data.msg,
                type: 'error'
              });
            }
          })
        } else {
          return false;
        }
      });
    },
    // 启用账号Enable
    EnableAccount() {
       if (undefined != this.selectId.length && 0 < this.selectId.length) {
        this.$confirm('此操作将启用该数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var params = new URLSearchParams();
          params.append('customerId', this.selectId);
          params.append('customerName', this.editInfoBefore.customerName);
          params.append('customerIsUsed','1');
          params.append('version', this.editInfo.version);
          this.openFullScreen();//打开遮罩
          this.$axios.post(this.IsUsedUrl, params).then(res => {
            this.loading.close(); //关闭加载
            if (0 == res.data.code) {//启用成功
              this.getData();
              this.$message({
                showClose: true,
                message: '启用成功',
                type: 'success'
              });
              this.dialogEdit = false;//隐藏dialo 
            } else {
              this.$message({
                showClose: true,
                message: res.data.msg,
                type: 'error'
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消启用'
          });
        });
      } else {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行启用",
          type: 'error'
        });
      }
    },
    // 禁用账号Enable
    DisEnableAccount() {
      if (undefined != this.selectId.length && 0 < this.selectId.length) {
        this.$confirm('此操作将禁用该数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var params = new URLSearchParams();
          params.append('userList', this.selectId);
          params.append('customerIsUsed','0');
          this.openFullScreen();//打开遮罩
          this.$axios.post(this.IsUsedUrl, params).then(res => {
            this.loading.close(); //关闭加载
            if (0 == res.data.code) {//启用成功
              //还剩的条数>当前页数减一乘每页条数且 当前页数不是第一页
              if (Number(this.dataSize) - Number(this.delNum) > Number(Number(this.pageNum) - 1) * Number(this.pageSize) && Number(this.pageNum) > 1) {//如果页数*每页条数 大于之前总条数减去删除的条数 即还剩的条数 则继续请求 否者 当前页数减一
                this.getData();
              } else {
                this.pageNum--;
              }
              this.editInfo = {};
              this.$message({
                type: 'success',
                message: '禁用成功!'
              });
            } else {
              this.$message({
                showClose: true,
                message: res.data.msg,
                type: 'error'
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消禁用'
          });
        });
      } else {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行禁用",
          type: 'error'
        });
      }
    },
    // 选择一条存取selectId
    chooseOne(val) {
      var customerId = [];
      for (var i = 0; i < val.length; i++) {
        customerId.push(val[i].customerId)
      }
      this.delNum = customerId.length;
      this.selectId = customerId;//将选中的id存起来
      if (1 == val.length) {//选中一条时将选中的值存起来 否则清空待修改
        this.editInfoBefore = JSON.parse(JSON.stringify(val[0]));
        this.getCustomerDetail(JSON.parse(JSON.stringify(val[0])).customerId);
      } else {
        this.editInfo = {};
        this.editInfoBefore = {};
      }
    },
    // 根据id查询内容  ==>用于修改时的表单显示
    getCustomerDetail(customerId){
       var params = new URLSearchParams();
      params.append('customerId', customerId);
      this.$axios.post(this.getCustomerDetailUrl, params).then(res => {
        this.editInfoBefore = {};
        if (0 == res.data.code) {//查询成功
          this.editInfoBefore = res.data.data;
        } else {
          this.$message({
            showClose: true,
            message: res.data.msg,
            type: 'error'
          });
        }
      })
    },
    //全选
    chooseAll(val) {
      var customerId = [];
      for (var i = 0; i < val.length; i++) {
        customerId.push(val[i].customerId)
      }
      this.delNum = customerId.length;
      this.selectId = customerId;//将选中的id存起来
      this.editInfo = {};
      this.editInfoBefore = {};
    },
    //每页条数
    handleSizeChange(val) {
      this.pageSize = val;
      this.getData();
    },
    //第几页
    handleCurrentChange(val) {
      this.pageNum = val;
      this.getData();
    },
    //每页条数
    handleSizeChangePost(val) {
      this.pageSizePost = val;
      this.getPostByDept();
    },
    //第几页
    handleCurrentChangePost(val) {
      this.pageNumPost = val;
      this.getPostByDept();
    },
    // 取消dialog
    cancelDialog() {
      this.dialogAdd = false;//隐藏新增dialo  
      this.dialogEdit = false;//修改dialo  
      if (this.$refs['editInfo']) {//清空表单
        this.$refs['editInfo'].resetFields();
      }
      if (this.$refs['formInlinePost']) {//清空表单
        this.$refs['formInlinePost'].resetFields();
      }
      if (1 != this.pageNumPost) {
        this.pageNumPost = 1;//每次查询从第一页开始
      }
    },
  }
}
</script>
<style scoped>
.handle-box {
  margin-bottom: 20px;
}
.accoutDialog .el-form-item__error {
  padding: 0;
}
.inputWidth {
  width: 400px;
}
</style>