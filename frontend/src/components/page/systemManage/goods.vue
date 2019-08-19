<template>
  <!-- stripe属性可以创建带斑马纹的表格 
        border属性可以创建竖直方向的边框 
        height属性可实现固定表头的表格
        fixed列冻结//参考apihttp://element-cn.eleme.io/#/zh-CN/component/table
        配置highlight-current-row属性即可实现单选。之后由current-change事件来管理选中时触发的事件，它会传入currentRow，oldCurrentRow。
        show-overflow-tooltip 超过部分。。。。
  -->
  <div>
    <div>
      <el-form
        :inline="true"
        :model="formInline"
        ref="formInline"
        class="demo-form-inline searchStyle"
      >
        <el-form-item label="一级类目" prop="categoryFirst">
          <el-select v-model="formInline.categoryFirst" clearable placeholder="请选择">
            <el-option
              v-for="item in optionsFirst"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="二级类目" prop="categorySecond">
          <el-select v-model="formInline.categorySecond" clearable placeholder="请选择">
            <el-option
              v-for="item in optionsSecond"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="商品编码" prop="commodityCode">
          <!--prop 重置时用到  -->
          <el-input v-model="formInline.commodityCode" clearable></el-input>
        </el-form-item>
        <el-form-item label="商品名称" prop="commodityName">
          <el-input v-model="formInline.commodityName" clearable></el-input>
        </el-form-item>
        <el-form-item label="是否上架" prop="commodityIsSold">
          <el-input v-model="formInline.commodityIsSold" clearable></el-input>
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
      <el-button type="primary" icon="el-icon-plus" @click="editGoods('editInfo')">修改</el-button>
      <el-button type="primary" icon="el-icon-edit" @click="upperShelf()">上架</el-button>
      <el-button type="primary" icon="el-icon-delete" @click="lowerShelf()">下架</el-button>
      <el-button type="primary" icon="el-icon-plus" @click="addGoods()">新增</el-button>
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
      <el-table-column type="selection" width="55" align="center"></el-table-column>
      <el-table-column prop="commodityCode" label="商品编号" fixed="left" width="100"></el-table-column>
      <el-table-column label="商品首图" width="120">
        <template slot-scope="scope">
          <img :src="scope.row.commodityFirstPicture" class="pic-img"/>
        </template>
      </el-table-column>
      <el-table-column prop="commodityName" label="商品名称" width="350"></el-table-column>
      <el-table-column prop="categoryFirst" label="一级类目"></el-table-column>
      <!-- <el-table-column prop="categoryFirstName" label="一级类目名称" width="100"></el-table-column> -->
      <el-table-column prop="categorySecond" label="二级类目"></el-table-column>
      <!-- <el-table-column prop="categorySecondName" label="二级类目名称"></el-table-column> -->
      <el-table-column prop="commodityRetailPrice" label="零售价"></el-table-column>
      <!-- <el-table-column prop="commodityOriginalPrice" label="原价" ></el-table-column> -->
      <el-table-column prop="commodityTotalCount" label="数量"></el-table-column>
      <el-table-column prop="commodityIsSold" label="是否上架" width="80"></el-table-column>
      <!-- <el-table-column prop="commodityId" label="商品id" width="80"></el-table-column> -->
      <!-- <el-table-column prop="commodityColor" label="颜色" width="100"></el-table-column> -->
      <!-- <el-table-column prop="commodityUnitId" label="商品单位id" width="100"></el-table-column> -->
      <!-- <el-table-column prop="commodityIsRecommend" label="是否推荐" width="100"></el-table-column> -->
      <!-- <el-table-column prop="version" label="版本号" width="100"></el-table-column> -->
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
      title="修改"
      :visible.sync="dialogEditGoods"
      :close-on-click-modal="false"
      class="editGoodsDialog"
    >
    <div class="editGoods-basic">
      <span class="basic-text">基本信息</span>
    </div>
      <el-form
        :model="editInfo"
        label-width="100px"
        
        ref="editInfo"
        :inline="true"
        :label-position="'right'"
      >
        <el-form-item label="一级类目" prop="categoryFirst">
          <el-input v-model="editInfo.categoryFirst" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="二级类目" prop="categorySecond">
          <el-input v-model="editInfo.categorySecond" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="商品名称" prop="commodityName">
          <el-input v-model="editInfo.commodityName" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="零售价" prop="commodityRetailPrice">
          <el-input v-model="editInfo.commodityRetailPrice" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="库存" prop="commodityInventory">
          <el-input v-model="editInfo.commodityInventory" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="是否上架" prop="commodityIsSold">
          <el-input v-model="editInfo.commodityIsSold" clearable class="inputWidth"></el-input>
        </el-form-item>
      </el-form>
      <div class="editGoods-pic">
        <span class="pic-text">轮播图添加</span>
      </div>
      <div class="picBox">
        <template slot-scope="scope">
          <img :src="scope.row.pictureList.pictureAddress"/>
        </template>
      </div>

      <div class="editGoods-setUp">
        <span class="setUp-text">设置详情</span>
      </div>
      <div class="setUpBox"></div>

      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">取 消</el-button>
        <el-button type="primary" @click="editGoodsSure('editInfo')">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      width="52%"
      title="新增"
      :visible.sync="dialogAddGoods"
      :close-on-click-modal="false"
      class="editGoodsDialog"
    >
    <div class="editGoods-basic">
      <span class="basic-text">基本信息</span>
    </div>
      <el-form
        :model="addGoodsInfo"
        label-width="100px"
        
        ref="addGoodsInfo"
        :inline="true"
        :label-position="'right'"
      >
        <el-form-item label="一级类目" prop="categoryFirst">
          <el-input v-model="addGoodsInfo.categoryFirst" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="二级类目" prop="categorySecond">
          <el-input v-model="addGoodsInfo.categorySecond" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="商品名称" prop="commodityName">
          <el-input v-model="addGoodsInfo.commodityName" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="零售价" prop="commodityRetailPrice">
          <el-input v-model="addGoodsInfo.commodityRetailPrice" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="原价" prop="commodityOriginalPrice">
          <el-input v-model="addGoodsInfo.commodityOriginalPrice" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="颜色" prop="commodityColor">
          <el-input v-model="addGoodsInfo.commodityColor" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="商品单位id" prop="commodityUnitId">
          <el-input v-model="addGoodsInfo.commodityUnitId" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="是否推荐" prop="commodityIsRecommend">
          <el-input v-model="addGoodsInfo.commodityIsRecommend" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="库存" prop="commodityInventory">
          <el-input v-model="addGoodsInfo.commodityInventory" clearable class="inputWidth"></el-input>
        </el-form-item>
        <el-form-item label="是否上架" prop="commodityIsSold">
          <el-input v-model="addGoodsInfo.commodityIsSold" clearable class="inputWidth"></el-input>
        </el-form-item>
      </el-form>
      <div class="editGoods-pic">
        <span class="pic-text">轮播图添加</span>
      </div>
      <div class="picBox">
        <template slot-scope="scope">
          <img :src="scope.row.pictureList.pictureAddress"/>
        </template>
      </div>

      <div class="editGoods-setUp">
        <span class="setUp-text">设置详情</span>
      </div>
      <div class="setUpBox"></div>

      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">取 消</el-button>
        <el-button type="primary" @click="addGoodsSure('addGoodsInfo')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: "", //加载遮罩
      data: [], //部门菜单
      defaultProps: {
        children: "children",
        label: "label"
      },
      dataSize: 0, //总条数
      tableData: [],
      optionsFirst: [ //一级分类下拉框
        {
          value: "1",
          label: "1"
        }
      ],
      optionsSecond: [//二级分类下拉框
        {
          value: "2",
          label: "2"
        }
      ],
      addGoodsInfo: {
        commodityName: '',
        categoryFirst: '',
        categorySecond: '',
        commodityRetailPrice: '',
        commodityOriginalPrice: '',
        commodityIsSold: '',
        commodityInventory: '',
        commodityColor: '',
        commodityUnitId: '',
        commodityIsRecommend: '',
        pictureList: [],
      },
      pageNum: 1,
      pageSize: 10,
      menuCode: "", //取store中的值
      menuButtonList: [], //菜单按钮列表
      formData: {}, //查询条件传值

      dialogEditGoods: false, //修改商品框默认隐藏
      dialogAddGoods: false,//新增商品框默认隐藏
      
      //叶展宏，网关commodityManager
      // getDataUrl:
      //   this.$store.state.url + "commodityManager/backend/goods/getGoodsList", //查询
      // editGoodsUrl: this.$store.state.url + "commodityManager/backend/goods/updateGoods", //修改商品
      // updateGoodsSellUrl: this.$store.state.url + "commodityManager/backend/goods/updateGoodsIsSell", //上架/下架
      // getGoodsDetailUrl: this.$store.state.url + "commodityManager/backend/goods/getGoodsDetail", //商品详情，修改用
      // addGoodsUrl: this.$store.state.url + "commodityManager/backend/goods/addGoods", //新增商品
      

      //叶楚义，网关systemManager/mall
      getDataUrl:
        this.$store.state.url + "systemManager/mall/backend/goods/getGoodsList", //查询
      editGoodsUrl: this.$store.state.url + "systemManager/mall/backend/goods/updateGoods", //修改商品
      updateGoodsSellUrl: this.$store.state.url + "systemManager/mall/backend/goods/updateGoodsIsSell", //上架/下架
      getGoodsDetailUrl: this.$store.state.url + "systemManager/mall/backend/goods/getGoodsDetail", //商品详情，修改用
      addGoodsUrl: this.$store.state.url + "systemManager/mall/backend/goods/addGoods", //新增商品

      formInline: {
        //快捷查询
        categoryFirst: "",
        categorySecond: "",
        commodityCode: "",
        commodityName: "",
        commodityIsSold: ""
      },
      editGoodsInfo: {},
      selectId: [], //选中的id
      editInfo: {}, //待修改的参数
      editInfoBefore: "", //修改前的值 取消修改用
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
    });
  },
  activated: function() {
    //  console.log( this.menuButtonList)
  },

  methods: {
    //打开加载
    // openFullScreen() {
    //   this.loading = this.$loading({
    //     lock: true,
    //     text: '操作中...',
    //     spinner: 'el-icon-loading',
    //     background: 'rgba(0, 0, 0, 0.7)'
    //   });
    // },

    //判断点击哪个按钮
    chooseClick(method) {
      if ("editGoods" == method) {  //修改商品
        this.editGoods("editInfo");
      } else if ("upperShelf" == method) {  //上架
        this.upperShelf();
      } else if ("lowerShelf" == method) {  //下架
        this.lowerShelf();
      }
    },
    //查询
    searchForm() {
      // var params = new URLSearchParams();
      // params.append("categoryFirst", this.formInline.categoryFirst);
      // params.append("categorySecond", this.formInline.categorySecond);
      // params.append("commodityCode", this.formInline.commodityCode);
      // params.append("commodityName", this.formInline.commodityName);
      // params.append("commodityIsSold", this.formInline.commodityIsSold);
      // this.formData = params;
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
    //修改商品
    editGoods(form) {
      if (this.editInfoBefore) {
        if (undefined != this.editInfoBefore.commodityId) {
          this.dialogEditGoods = true;
          //商品详情
          var params = {
            'commodityId': this.editInfoBefore.commodityId,
          };
          this.$axios.get(this.getGoodsDetailUrl, params).then(res => {
            // this.loading.close(); //关闭加载
            this.editInfoBefore = {};
            this.selectId = {};
            if (0 == res.data.code) {//查询成功
              this.editInfo = res.data.data;
            } else {
              this.$message({
                showClose: true,
                message: res.data.msg,
                type: 'error'
              });
            }
          });
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
    //确认修改商品
    editGoodsSure(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          var params = new URLSearchParams();
          params.append("commodityId", this.editInfo.commodityId);
          params.append("commodityName", this.editInfo.commodityName);
          params.append("categoryFirst", this.editInfo.categoryFirst);
          params.append("categorySecond", this.editInfo.categorySecond);
          params.append("commodityRetailPrice", this.editInfo.commodityRetailPrice);
          params.append("commodityOriginalPrice", this.editInfo.commodityOriginalPrice);
          params.append("commodityIsSold", this.editInfo.commodityIsSold);
          params.append("commodityInventory", this.editInfo.commodityInventory);
          params.append("commodityColor", this.editInfo.commodityColor);
          params.append("commodityUnitId", this.editInfo.commodityUnitId);
          params.append("commodityIsRecommend", this.editInfo.commodityIsRecommend);
          params.append("version", this.editInfo.version);

          // this.openFullScreen(); //打开遮罩
          this.$axios.post(this.editGoodsUrl, params).then(res => {
            // this.loading.close(); //关闭加载
            if (0 == res.data.code) {
              //修改成功
              this.getData();
              this.$message({
                showClose: true,
                message: "修改商品成功",
                type: "success"
              });
              this.dialogEditGoods = false; //隐藏dialo
              this.$refs[editInfo].resetFields(); //清除待修改数据
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
    //新增商品
    addGoods(form) {
      this.dialogAddGoods = true;
      if (this.$refs[addGoodsInfo]) {//清空表单
        this.$refs[addGoodsInfo].resetFields();
      }
    },
    //确认新增商品
    addGoodsSure(formName) {
      console.log(this.addGoodsInfo);
      this.$refs[formName].validate(valid => {
        if (valid) {
          var params = new URLSearchParams();
          params.append("commodityName", this.addGoodsInfo.commodityName);
          params.append("categoryFirst", this.addGoodsInfo.categoryFirst);
          params.append("categorySecond", this.addGoodsInfo.categorySecond);
          params.append("commodityRetailPrice", this.addGoodsInfo.commodityRetailPrice);
          params.append("commodityOriginalPrice", this.addGoodsInfo.commodityOriginalPrice);
          params.append("commodityIsSold", this.addGoodsInfo.commodityIsSold);
          params.append("commodityInventory", this.addGoodsInfo.commodityInventory);
          params.append("commodityColor", this.addGoodsInfo.commodityColor);
          params.append("commodityUnitId", this.addGoodsInfo.commodityUnitId);
          params.append("commodityIsRecommend", this.addGoodsInfo.commodityIsRecommend);
          // this.openFullScreen(); //打开遮罩
          this.$axios.post(this.addGoodsUrl, params).then(res => {
            // this.loading.close(); //关闭加载
            if (0 == res.data.code) {
              //添加成功
              this.getData();
              this.$message({
                showClose: true,
                message: "添加商品成功",
                type: "success"
              });
              this.dialogAddGoods = false; //隐藏dialo
              this.$refs[addGoodsInfo].resetFields(); //清除待修改数据
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
      this.dialogEditGoods = false; //隐藏新增dialo
      if (this.$refs["editInfo"]) {
        //清空表单
        this.$refs["editInfo"].resetFields();
      }
      if (this.$refs["addGoodsInfo"]) {
        //清空表单
        this.$refs["addGoodsInfo"].resetFields();
      }
      if (1 != this.pageNumPost) {
        this.pageNumPost = 1; //每次查询从第一页开始
      }
      this.dialogEditGoods = false;
      this.dialogAddGoods = false;
    },
    //下架
    lowerShelf() {
      if (this.selectId.length != 1) {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行操作",
          type: "error"
        });
      } else {
        if (undefined != this.selectId.length && 0 < this.selectId.length) {
          this.$confirm("确认下架该商品, 是否继续?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
          })
          .then(() => {
            var params = new URLSearchParams();
            params.append("commodityId", this.selectId[0].commodityId);
            params.append("commodityIsSold", "0");
            params.append("version", this.selectId[0].version);
            // this.openFullScreen(); //打开遮罩
            this.$axios.post(this.updateGoodsSellUrl, params).then(res => {
              // this.loading.close(); //关闭加载
              if (0 == res.data.code) {
                this.getData();
                this.editInfo = {};
                this.$message({
                  type: "success",
                  message: "下架成功!"
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
              message: "已取消操作"
            });
          });
        } else {
          this.$message({
            showClose: true,
            message: "请选择一条数据进行操作",
            type: "error"
          });
        }
      }
    },
    //上架
    upperShelf() {
      if (this.selectId.length != 1) {
        this.$message({
          showClose: true,
          message: "请选择一条数据进行操作",
          type: "error"
        });
      } else {
        if (undefined != this.selectId.length && 0 < this.selectId.length) {
          this.$confirm("确认上架该商品, 是否继续?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
          })
          .then(() => {
            var params = new URLSearchParams();
            params.append("commodityId", this.selectId[0].commodityId);
            params.append("commodityIsSold", "1");
            params.append("version", this.selectId[0].version);
            // this.openFullScreen(); //打开遮罩
            this.$axios.post(this.updateGoodsSellUrl, params).then(res => {
              // this.loading.close(); //关闭加载
              if (0 == res.data.code) {
                this.getData();
                this.editInfo = {};
                this.$message({
                  type: "success",
                  message: "上架成功!"
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
              message: "已取消操作"
            });
          });
        } else {
          this.$message({
            showClose: true,
            message: "请选择一条数据进行操作",
            type: "error"
          });
        }
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
    //选中checkbox，取消选中 此处返回的是以选中的val
    chooseOne(val) {
      var selectData = [];
      for (var i = 0; i < val.length; i++) {
        selectData.push(val[i]);
      }
      this.selectId = selectData; //将选中的数据存起来到全局变量selectId
      if (1 == val.length) {
        //选中一条时将选中的值存起来 否则清空待修改
        this.editInfoBefore = JSON.parse(JSON.stringify(val[0]));
      } else {
        this.editInfo = {};
        this.editInfoBefore = {};
      }
    },
    //全选
    chooseAll(val) {
      var selectData = [];
      for (var i = 0; i < val.length; i++) {
        selectData.push(val[i].selectData);
      }
      this.selectId = selectData; //将选中的数据存起来到全局变量selectId
      this.editInfo = {};
      this.editInfoBefore = {};
    },
    getData() {
      var params = {
        "categoryFirst": this.formInline.categoryFirst,
        "categorySecond": this.formInline.categorySecond,
        "commodityCode":this.formInline.commodityCode,
        "commodityName":this.formInline.commodityName,
        "commodityIsSold":this.formInline.commodityIsSold,
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
          // this.loading.close(); //关闭加载
          if (0 == res.data.code) {
            //查询成功
            this.tableData = res.data.data.list;
            this.dataSize = res.data.data.totalRecords;
          } else {
            this.$message({
              showClose: true,
              message: res.data.msg,
              type: "error"
            });
          }
        });
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
}
.el-form-item {
  margin-bottom: 15px;
}


.editGoods-basic,.editGoods-pic,.editGoods-setUp {
  width: 97%;
  height: 40px;
  margin: 0 auto;
  margin-bottom: 15px;
  background-color: rgb(228, 228, 228);
}
.editGoods-pic,.editGoods-setUp {
  margin-bottom: 0;
  border-left: 1px solid rgb(228, 228, 228);
  border-right: 1px solid rgb(228, 228, 228);
}
.basic-text,.pic-text,.setUp-text {
    line-height: 40px;
    margin-left: 10px;
    font-weight: 600;
}
.picBox,.setUpBox {
    width: 97%;
    height: 100px;
    margin: 0 auto;
    border: 1px solid rgb(228, 228, 228);
}
.picBox {
  margin-bottom: 15px;
}
.pic-img {
  display: flex;
  width: 50px;
  height: 50px;
  margin: 0 auto;
}
</style>
<style>
.autoWidth .el-dialog {
  width: 650px;
}
.changePassword .inputWidth {
  width: 250px;
}
.editGoodsDialog .el-form-item__error {
  padding: 0;
}
.changePassword .el-form-item__error {
  padding: 0;
}
.searchStyle .el-form-item__label {
  line-height: 40px;
}
.searchStyle .el-form-item__content {
  line-height: 40px;
}
.searchStyle .el-input-icon {
  line-height: 40px;
}
</style>