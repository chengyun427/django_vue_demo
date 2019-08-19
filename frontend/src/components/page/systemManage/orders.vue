<template>
  <div>
    <div>
      <el-form
        :inline="true"
        :model="formInline"
        ref="formInline"
        class="demo-form-inline searchStyle"
      >
        <el-form-item label="订单号" prop="orderNumber">
          <!--prop 重置时用到  -->
          <el-input v-model="formInline.orderNumber" clearable></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="orderState">
          <el-select v-model="formInline.orderState" clearable placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期" prop="orderDateStart">
          <el-date-picker
            class="inputWidth"
            v-model="formInline.orderDateStart"
            type="date"
            clearable
            placeholder="选择日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="-" prop="orderDateEnd">
          <el-date-picker
            class="inputWidth"
            v-model="formInline.orderDateEnd"
            type="date"
            clearable
            placeholder="选择日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchForm()">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="resetForm('formInline')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="handle-box">
      <el-button type="primary" icon="el-icon-search" @click="searchDetail('detailInfo')">查看详情</el-button>
    </div>
    <el-table
      :data="tableData"
      border
      stripe
      @select="chooseOne"
      @select-all="chooseAll"
      style="width: 100%"
    >
      <!--  ref="multipleTable" -->
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="orderNumber" label="订单号" fixed="left" sortable width="300"></el-table-column>
      <el-table-column prop="orderPrice" label="实际金额" width="200"></el-table-column>
      <el-table-column prop="customerName" label="下单人" width="200"></el-table-column>
      <el-table-column prop="orderState" label="订单状态" width="200"></el-table-column>
      <el-table-column prop="orderDate" label="订单时间" :formatter="dateFormat"></el-table-column>
    </el-table>
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
    <el-dialog
      width="52%"
      title="查看"
      :visible.sync="dialogDetail"
      :close-on-click-modal="false"
      class="userDialog"
    >
      <div class="small-top">订单详情</div>
      <el-form
        :model="detailInfo"
        label-width="100px"
        :rules="rules"
        ref="detailInfo"
        :inline="true"
        :label-position="'right'"
      >
        <el-form-item label="订单编号" prop="orderNumber">
          <el-input v-model="detailInfo.orderNumber" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="下单人" prop="customerName">
          <el-input v-model="detailInfo.customerName" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="订单日期" prop="orderDate">
          <el-input v-model="detailInfo.orderDate" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="收货地址" prop="orderAddress">
          <el-input v-model="detailInfo.orderAddress" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="运费" prop="phone">
          <el-input v-model="detailInfo.phone" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="发货留言" prop="orderRemark">
          <el-input type="textarea" v-model="detailInfo.orderRemark" clearable style="width:400px"></el-input>
        </el-form-item>
      </el-form>
      <div class="small-top">订单详情</div>
      <el-table
        :data="detailData"
        border
        stripe
        @select="chooseOne"
        @select-all="chooseAll"
        style="width: 100%"
      >
        <!--  ref="multipleTable" -->
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="commodityFirstPicture" label="商品首图" width="150"></el-table-column>
        <el-table-column prop="commodityName" label="商品名称" width="170"></el-table-column>
        <el-table-column prop="commodityCode" label="商品编码" width="120"></el-table-column>
        <el-table-column prop="commodityPrice" label="单价" width="90"></el-table-column>
        <el-table-column prop="commodityNum" label="数量" width="90"></el-table-column>
        <el-table-column prop="commodityTotalPrice" label="小计"></el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="cancelDialog()">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    //表单验证飞控去空格后非空
    var validatePass = (rule, value, callback) => {
      if (value.replace(/(^\s*)|(\s*$)/g, "") === "") {
        //前后去空格
        callback(new Error("请输入用户名称"));
      } else {
        callback();
      }
    };
    //修改
    var validatePass2 = (rule, value, callback) => {
      if (value.replace(/(^\s*)|(\s*$)/g, "") === "") {
        //前后去空格
        callback(new Error("请输入用户账号"));
      } else {
        callback();
      }
    };
    //密码
    var validatePassWord = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.editPwd.passWordCheck !== "") {
          this.$refs.editPwd.validateField("passWordCheck");
        }
        callback();
      }
    };
    //密码确认
    var validatePassWordCheck = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.editPwd.passWord) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      loading: "", //加载遮罩
      dataSize: 0, //总条数
      dataSizePost: 0, //总条数

      //自己写的查看详情的数据
      dialogDetail: false,
      detailInfo: [],
      detailData: [],
      tableData: [],
      options: [
        {
          value: '1',
          label: '待发货'
        },
        {
          value: '2',
          label: '已发货'
        },
        {
          value:'3',
          label:'已完成'
        },
        {
          value:'4',
          label:'已撤销'
        }
      ],
      pageNum: 1,
      pageSize: 10,
      formData: {}, //查询条件传值
      getDataUrl:
        this.$store.state.url + "orderManagement/backend/order/getOrders", //查询
      getDetailUrl:
        this.$store.state.url + "orderManagement/backend/order/getOrderDetail", //查看详情

      formInline: {
        //快捷查询
        orderNumber: "",
        orderState: "",
        orderDateStart: "",
        orderDateEnd: ""
      },
      selectId: [], //选中的id
      editInfoBefore: "", //修改前的值 取消修改用
      i: 0,
      rules: {
        //表单验证
        userAcct: [
          { required: true, validator: validatePass2, trigger: "blur" }, // //,
          { min: 1, max: 40, message: "长度在 1 到 40 个字符", trigger: "blur" }
        ],
        userName: [
          { required: true, validator: validatePass, trigger: "blur" },
          { min: 1, max: 40, message: "长度在 1 到 40 个字符", trigger: "blur" }
        ],
        idCard: [
          //身份证验证
          {
            pattern: /(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)/,
            message: "证件号码格式有误！",
            trigger: "blur"
          }
        ],
        tel: [
          //固定电话
          {
            pattern: /^((0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/,
            message: "请输入正确的固定电话",
            trigger: "blur"
          }
        ],
        phone: [
          //手机号码
          {
            pattern: /^[1][3,4,5,7,8][0-9]{9}$/,
            message: "请输入正确的手机号码",
            trigger: "blur"
          }
        ],
        email: [
          //电子邮箱
          {
            pattern: /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/,
            message: "请输入正确电子邮箱",
            trigger: "blur"
          }
        ],
        deptName: [],
        ip: [
          //IP地址
          {
            pattern: /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/,
            message: "请输入正确的IP",
            trigger: "blur"
          }
        ],
        remark: [
          //备注无需验证 写在此处是为了打开tialog时能统一清空表单
          {
            min: 1,
            max: 200,
            message: "长度在 1 到 200 个字符",
            trigger: "blur"
          }
        ]
      },
    };
  },
  watch: {
    pageNum: function() {
      this.getData();
    },
    pageSize: function() {
      this.getData();
    }
  },
  mounted: function() {
    this.$nextTick(function() {
      this.getData(); //获取页面表格
      //this.getButton();//获取页面按钮
    });
  },

  methods: {
    //打开加载
    openFullScreen() {
      this.loading = this.$loading({
        lock: true,
        text: "操作中...",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)"
      });
    },
    //获取页面按钮
    getButton() {
      this.menuCode = this.$store.state.menuCode; //防止按钮下面还有权限 切换菜单时值会改变
      var params = new URLSearchParams();
      params.append("USER_NAME", localStorage.getItem("ms_username"));
      params.append("MENU_CODE", this.menuCode);
      params.append("BUTTON_CODE", "");
      this.$axios.post(this.$store.state.getButtonUrl, params).then(res => {
        if (0 == res.data.code) {
          //设置成功
          this.menuButtonList = res.data.data;
        } else {
          this.$message({
            showClose: true,
            message: res.data.msg,
            type: "error"
          });
        }
      });
    },
    //判断点击哪个按钮
    chooseClick(method) {
      if ("addUser" == method) {
        this.addUser("addInfo");
      } else if ("editNews" == method) {
        this.editNews();
      } else if ("delUser" == method) {
        this.delUser();
      } else if ("assignRole" == method) {
        this.assignRole();
      } else if ("setPost" == method) {
        this.setPost();
      } else if ("setDepartment" == method) {
        this.setDepartment();
      } else if ("searchDetail" == method) {
        this.searchDetail("addInfo");
      }
    },
    //查询
    searchForm() {
      var params = new URLSearchParams();
      //   params.append("formData",JSON.stringify({
      //     userAcct: this.formInline.userAcct,
      //     userName: this.formInline.userName
      //  }));
      params.append("orderNumber", this.formInline.orderNumber);
      params.append("orderState", this.formInline.orderState);
      params.append("orderDateStart", this.formInline.orderDateStart);
      params.append("orderDateEnd", this.formInline.orderDateEnd);
      this.formData = params;
      // this.pageNum=1;//每次查询从第一页开始
      // this.getData();
      if (1 != this.pageNum) {
        this.pageNum = 1; //每次查询从第一页开始
      } else {
        this.getData();
      }
    },

    //重置查询域
    resetForm(formInline) {
      this.$refs[formInline].resetFields();
    },
    //查询-设置岗位
    searchFormPost() {
      var params = new URLSearchParams();
      params.append("postName", this.formInlinePost.postName);
      this.formData = params;
      if (1 != this.pageNumPost) {
        this.pageNumPost = 1; //每次查询从第一页开始
      } else {
        this.getPostByDept();
      }
    },
    //重置查询域-设置岗位
    resetFormPost(formInlinePost) {
      this.$refs[formInlinePost].resetFields();
    },
    //用户新增
    addUser(addInfo) {
      this.dialogAdd = true;
      if (this.$refs[addInfo]) {
        //清空表单
        this.$refs[addInfo].resetFields();
      }
    },

    //查看详情方法
    searchDetail() {
      if (this.editInfoBefore) {
        if (1 == this.selectId.length) {
          this.dialogDetail = true;
          this.detailInfo = JSON.parse(JSON.stringify(this.editInfoBefore));
          var params = new URLSearchParams();
          // params.append("orderId", this.editInfoBefore.orderId);
          this.$axios
            .get(
              this.getDetailUrl + "?orderId=" + this.editInfoBefore.orderId,
              params
            )
            .then(res => {
              if (0 == res.data.code) {
                this.detailData = res.data.data.commodityList;//获取商品详情信息
              }
            });
        } else {
          this.$message({
            showClose: true,
            message: "请选择一条数据进行查看",
            type: "error"
          });
        }
      } else {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行查看",
          type: "error"
        });
      }
      // console.log(this.detailInfo);
      // console.log(this.detailInfo.orderId);
      console.log(this.detailData);
    },
    //新增-选择部门 树
    openTreeChooseAdd() {
      this.getDeptData();
      this.innerVisibleAdd = true;
      // this.chooseDept={};//清空已选部门树
    },
    //修改-选择部门树
    openTreeChooseEdit() {
      this.defautChoose = [];
      this.defautChoose = [this.editInfoBefore.deptCode]; //默认选中当前所属部门
      this.chooseDept.id = this.editInfoBefore.deptCode;
      this.chooseDept.label = this.editInfoBefore.label;
      this.getDeptData();
      this.innerVisibleEdit = true;
      //   this.chooseDept={};//清空已选部门树
    },
    //选中一条 部门树
    handleNodeClick(data) {
      this.chooseDept = data;
    },
    //新增确认选择部门 树
    addChooseSure(val) {
      if (this.chooseDept.id) {
        if (1 == val) {
          //1是新增 2是修改
          this.deptName = this.chooseDept.label;
          this.innerVisibleAdd = false;
        } else {
          if (0 < this.$refs.tree1.getCheckedKeys().length) {
            this.editInfo.deptName = this.chooseDept.label;
            this.innerVisibleEdit = false;
          } else {
            this.$message({
              showClose: true,
              message: "请选择一个部门",
              type: "error"
            });
          }
        }
      } else {
        this.$message({
          showClose: true,
          message: "请选择一个部门",
          type: "error"
        });
      }
    },
    //获取部门树
    getDeptData() {
      this.chooseDept = {}; //清空已选部门树
      this.$axios.post(this.getMenuUrl).then(res => {
        if (0 == res.data.code) {
          //查询成功
          this.data = res.data.data;
        } else {
          this.$message({
            showClose: true,
            message: res.data.msg,
            type: "error"
          });
        }
      });
    },
    //新增修改——岗位——tree
    cancelTreeDialog() {
      this.innerVisibleAdd = false; //修改dialo
      this.innerVisibleEdit = false; //修改dialo
    },
    //确认新增
    addSure(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          var params = new URLSearchParams();
          params.append("userAccount", this.addInfo.userAcct);
          params.append("userName", this.addInfo.userName);
          params.append("userIdNumber", this.addInfo.idCard);
          params.append("userGender", this.addInfo.sex);
          params.append("tel", this.addInfo.tel);
          params.append("userTel", this.addInfo.phone);
          params.append("userEmail", this.addInfo.email);
          params.append("isAdmin", this.addInfo.isAdmin);
          params.append("userPwd", this.addInfo.userPwd);
          params.append("deptCode", this.chooseDept.id);
          //params.append('ip', this.addInfo.ip);
          params.append("userComments", this.addInfo.remark);
          this.openFullScreen(); //打开遮罩
          this.$axios.post(this.addUrl, params).then(res => {
            this.loading.close(); //关闭加载
            if (0 == res.data.code) {
              //新增成功
              this.getData();
              this.$message({
                showClose: true,
                message: "新增用户成功",
                type: "success"
              });
              this.dialogAdd = false; //隐藏dialo
            } else {
              this.$message({
                showClose: true,
                message: res.data.msg,
                type: "error"
              });
            }
          });
        } else {
          return false;
        }
      });
    },

    //取消新增，修改，修改密码
    cancelDialog() {
      this.dialogDetail = false; //隐藏详情dialo
      this.dialogAdd = false; //隐藏新增dialo
      this.dialogEdit = false; //修改dialo
      // if (this.$refs["editInfo"]) {
      //   //清空表单
      //   this.$refs["editInfo"].resetFields();
      // }
      if (this.$refs["formInlinePost"]) {
        //清空表单
        this.$refs["formInlinePost"].resetFields();
      }
      this.dialogPwdEdit = false; //隐藏修改密码dialo
      if (1 != this.pageNumPost) {
        this.pageNumPost = 1; //每次查询从第一页开始
      }
    },
    //修改信息
    editNews(form) {
      if (this.editInfoBefore) {
        if (undefined != this.editInfoBefore.id) {
          this.dialogEdit = true;
          this.editInfo = JSON.parse(JSON.stringify(this.editInfoBefore));
        } else {
          this.$message({
            showClose: true,
            message: "请选择一条数据进行修改",
            type: "error"
          });
        }
      } else {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行修改",
          type: "error"
        });
      }
    },
    //确认修改
    editSure(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          var params = new URLSearchParams();
          params.append("userCode", this.editInfo.userCode);
          params.append("userAcct", this.editInfo.userAcct);
          params.append("userName", this.editInfo.userName);
          params.append("idCard", this.editInfo.idCard);
          params.append("sex", this.editInfo.sex);
          params.append("isAdmin", this.editInfo.isAdmin);
          params.append("tel", this.editInfo.tel);
          params.append("phone", this.editInfo.phone);
          params.append("email", this.editInfo.email);
          // params.append('adminFlag', this.editInfo.adminFlag=='是'?1:0);
          params.append("deptCode", this.chooseDept.id);
          //params.append('ip', this.editInfo.ip);
          params.append("remark", this.editInfo.remark);
          params.append("version", this.editInfo.version);
          this.openFullScreen(); //打开遮罩
          this.$axios.post(this.editUrl, params).then(res => {
            this.loading.close(); //关闭加载
            if (0 == res.data.code) {
              //修改成功
              this.getData();
              this.$message({
                showClose: true,
                message: "修改用户成功",
                type: "success"
              });
              this.dialogEdit = false; //隐藏dialo
            } else {
              this.$message({
                showClose: true,
                message: res.data.msg,
                type: "error"
              });
            }
          });
        } else {
          return false;
        }
      });
    },
    //删除用户
    delUser() {
      if (undefined != this.selectId.length && 0 < this.selectId.length) {
        this.$confirm("此操作将永久删除该数据, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            var params = new URLSearchParams();
            params.append("userList", this.selectId);
            this.openFullScreen(); //打开遮罩
            this.$axios.post(this.delUrl, params).then(res => {
              this.loading.close(); //关闭加载
              if (0 == res.data.code) {
                //删除成功
                //还剩的条数>当前页数减一乘每页条数且 当前页数不是第一页
                if (
                  Number(this.dataSize) - Number(this.delNum) >
                    Number(Number(this.pageNum) - 1) * Number(this.pageSize) &&
                  Number(this.pageNum) > 1
                ) {
                  //如果页数*每页条数 大于之前总条数减去删除的条数 即还剩的条数 则继续请求 否者 当前页数减一
                  this.getData();
                } else {
                  this.pageNum--;
                }
                this.editInfo = {};
                this.$message({
                  type: "success",
                  message: "删除成功!"
                });
              } else {
                this.$message({
                  showClose: true,
                  message: res.data.msg,
                  type: "error"
                });
              }
            });
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除"
            });
          });
      } else {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行删除",
          type: "error"
        });
      }
    },
    //指派角色 radio变化监听
    chooseRadio() {
      if (
        -1 == this.roleForm.type.indexOf(this.roleForm.resource) &&
        "" != this.roleForm.resource
      ) {
        //查找数据所在的下标，如果没找到，返回-1
        this.roleForm.type.push(this.roleForm.resource); //即如果选中的radio前面的没选中 则选中
      }
    },
    //指派角色 check变化监听
    chooseCheck() {
      if (-1 == this.roleForm.type.indexOf(this.roleForm.resource)) {
        //查找数据所在的下标，如果没找到，返回-1
        this.roleForm.resource = "";
      }
    },
    //获取已授权的部门
    getHasUseDept() {
      var params = new URLSearchParams();
      params.append("userCode", this.editInfoBefore.userCode);
      this.$axios.post(this.hasUseDept, params).then(res => {
        if (0 == res.data.code) {
          //查询成功
          this.defautChoose = res.data.data;
          this.editInfoBefore.deptCode = this.defautChoose;
          this.chooseDept.id = this.editInfoBefore.deptCode;
        }
      });
    },
    //设置部门
    setDepartment() {
      this.defautChoose = [];
      if (this.editInfoBefore) {
        if (undefined != this.editInfoBefore.id) {
          this.getDeptData(); //获取部门树
          this.getHasUseDept(); //获取已授权的部门
          this.titleUserName = this.editInfoBefore.userName;
          // this.defautChoose=[this.editInfoBefore.deptCode];//默认选中当前所属部门
          // this.chooseDept.id=this.editInfoBefore.deptCode;
        } else {
          this.$message({
            showClose: true,
            message: "请选择一条数据进行设置部门",
            type: "error"
          });
        }
      } else {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行设置部门",
          type: "error"
        });
      }
    },
    //选择部门-设置部门
    handleNodeClick2(data) {
      this.$refs.tree2.setCheckedKeys([data.id]);
      this.chooseDept = data;
    },
    //选择部门-设置部门-check
    chooseOneDept(data, checked) {
      if (true == checked) {
        this.$refs.tree2.setCheckedKeys([]);
        this.handleNodeClick2(data);
      }
    },
    //选择部门-修改信息
    handleNodeClick1(data) {
      this.$refs.tree1.setCheckedKeys([data.id]);
      this.chooseDept = data;
    },
    //选择部门-修改信息-check
    chooseOneDept1(data, checked) {
      if (true == checked) {
        this.$refs.tree1.setCheckedKeys([]);
        this.handleNodeClick1(data);
      }
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
    //选中checkbox，取消选中 此处返回的是以选中的val
    chooseOne(val) {
      var userCode = [];
      for (var i = 0; i < val.length; i++) {
        userCode.push(val[i].userCode);
        console.log(userCode);
      }
      this.delNum = userCode.length;
      this.selectId = userCode; //将选中的id存起来
      if (1 == val.length) {
        //选中一条时将选中的值存起来 否则清空待修改
        this.editInfoBefore = JSON.parse(JSON.stringify(val[0]));
        //this.getUserByUserCode(JSON.parse(JSON.stringify(val[0])).userCode);
      } else {
        this.editInfo = {};
        this.editInfoBefore = {};
      }
      console.log(this.editInfoBefore);
      console.log(this.editInfoBefore.orderId);
    },
    //全选
    chooseAll(val) {
      var userCode = [];
      for (var i = 0; i < val.length; i++) {
        userCode.push(val[i].userCode);
      }
      this.delNum = userCode.length;
      this.selectId = userCode; //将选中的id存起来
      this.editInfo = {};
      this.editInfoBefore = {};
    },
    getData() {
      this.openFullScreen(); //打开遮罩
      var params = {
        orderNumber: this.formInline.orderNumber,
        orderState: this.formInline.orderState,
        orderDateStart: this.formInline.orderDateStart,
        orderDateEnd: this.formInline.orderDateEnd
      };
      this.$axios
        .get(
          this.getDataUrl +
            "?pageSize=" +
            this.pageSize +
            "&pageNum=" +
            this.pageNum,
          params
        )
        .then(res => {
          this.loading.close(); //关闭加载
          this.editInfoBefore = {};//修改前的值 取消修改用
          this.selectId = {};//选中的id
          if (0 == res.data.code) {
            //查询成功
            this.tableData = res.data.data.list;
            console.log(this.tableData);
            for (var i = 0; i < this.tableData.length; i++) {
              if (1 == this.tableData[i].orderState) {
                this.tableData[i].orderState = "待发货";
              } else if (2 == this.tableData[i].orderState) {
                this.tableData[i].orderState = "已发货";
              } else if (3 == this.tableData[i].orderState) {
                this.tableData[i].orderState = "已完成";
              } else {
                this.tableData[i].orderState = "已撤销";
              }
            }
            this.dataSize = res.data.data.totalRecords;//获取数据的页面总数
          } else {
            this.$message({
              showClose: true,
              message: res.data.msg,
              type: "error"
            });
          }
        });
    },
    getUserByUserCode(userCode) {
      var params = new URLSearchParams();
      params.append("userCode", userCode);
      this.$axios.post(this.getUserByUserCodeUrl, params).then(res => {
        this.editInfoBefore = {};
        if (0 == res.data.code) {
          //查询成功
          this.editInfoBefore = res.data.data;
        } else {
          this.$message({
            showClose: true,
            message: res.data.msg,
            type: "error"
          });
        }
      });
    },
    //时间格式化
    dateFormat(row, column) {
      var date = row[column.property];
      if (date == undefined) {
        return "";
      }
      return this.$moment(date).format("YYYY-MM-DD HH:mm:ss");
    }
  }
};
</script>

<style scoped>
.handle-box {
  margin-bottom: 20px;
}
.mar_top_12 {
  margin-top: 12px;
}
.roleStyle {
  width: 250px;
  height: 35px;
  line-height: 35px;
  float: left;
  text-align: center;
  border: 1px solid #d1dbe5;
}
.topNoStyle {
  border-top: none;
}
.rightNoStyle {
  border-right: none;
}
.tdStyle {
  width: 250px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border: 1px solid #d1dbe5;
  border-top: none;
  /* border-right:none */
}
.el-form-item {
  margin-bottom: 15px;
}
</style>
<style>
.autoWidth .el-dialog {
  width: 650px;
}
.changePassword .inputWidth {
  width: 250px;
}
.inputWidth .el-input__icon {
  line-height: 0px;
}
.small-top {
  margin: 10px 0px;
  padding: 0px 0px 0px 5px;
  width: 765px;
  height: 25px;
  line-height: 25px;
  background: #e6e6e6;
}
.userDialog .el-form-item__error {
  padding: 0;
}
.changePassword .el-form-item__error {
  padding: 0;
}
.searchStyle .el-form-item__label {
  line-height: 30px;
}
.searchStyle .el-form-item__content {
  line-height: 30px;
}
.searchStyle .el-input__icon{
  line-height: 30px;
}
</style>