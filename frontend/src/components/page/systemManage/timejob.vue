<template>
     <div>
    <div>
      <el-form :inline="true" :model="formInline" ref="formInline" class="demo-form-inline">
        <el-form-item label="任务名称"  prop="jobName"> <!--prop 重置时用到  -->
          <el-input v-model="formInline.jobName" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchForm()">查询</el-button>
        </el-form-item>
         <el-form-item>
          <el-button @click="resetForm('formInline')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
     <div  class="handle-box">
        <!-- <el-button type="primary" icon="el-icon-plus"    @click="addJob('addInfo')">新增</el-button>
        <el-button type="primary" icon="el-icon-edit"    @click="editJob">修改</el-button>
        <el-button type="primary" icon="el-icon-close"    @click="stopJob">停用</el-button>
        <el-button type="primary" icon="el-icon-check"  @click="starJob">启用</el-button>
        <el-button type="primary" icon="el-icon-delete"   @click="delJob">作废</el-button>
        <el-button type="primary" icon="el-icon-search" @click="findHistory">查看执行记录</el-button> -->
        <el-button v-for="(x,k) in menuButtonList" type="primary" :key="k" :icon=x.buttonStyle   @click="chooseClick(x.buttonUrl)">{{x.buttonName}}</el-button>
    </div>
    <el-table 
        :data="tableData" 
        border
        stripe 
        height="380" 
        style="width: 100%" 
        ref="multipleTable"
        highlight-current-row
        @current-change="chooseOne">
        <el-table-column prop="jobName" label="任务名称" sortable>
        </el-table-column>
        <el-table-column prop="description" label="任务描述" >
        </el-table-column>
        <el-table-column prop="serviceId" label="服务ID" >
        </el-table-column>
         <el-table-column prop="url" label="服务调用地址">
        </el-table-column>
        <el-table-column prop="cron" label="时间表达式" >
        </el-table-column>
         <!-- <el-table-column prop="sync" label="是否允许同步" >
        </el-table-column> -->
         <el-table-column prop="status" label="运行状态">
        </el-table-column>
    </el-table>
         
       
    <el-dialog title="新增任务" :visible.sync="dialogAdd" :close-on-click-modal="false">
       <el-dialog width="45%" title="时间表达式设置" :visible.sync="innerVisibleAdd" :close-on-click-modal="false" append-to-body>
        <div>
          <div>
            <el-radio-group v-model="timeRadio">
                <el-radio  :label="0" border>每分钟</el-radio>
                <el-radio  :label="1" border>每小时</el-radio>
                <el-radio  :label="2" border>每天</el-radio>
                <el-radio  :label="3" border>每周</el-radio>
                <el-radio  :label="4" border>每月</el-radio>
                <el-radio  :label="5" border>每年</el-radio>
              </el-radio-group>
          </div>
          <div style="margin-top:40px">
             <div v-if="timeRadio==0" >
               执行时间  <el-input-number 
                        style="width:100px" 
                        v-model="workTime.day0" 
                        controls-position="right" 
                        :min="1" :max="60"
                        >
                        </el-input-number>
               <!-- <el-input v-model="workTime.day0" clearable  class="inputWidth"/> -->
               <span style="color:red;margin-left:10px">(提示：每隔几分钟执行一次，即输入几)</span>
             </div>
             <div v-if="timeRadio==1" >
               执行时间  <el-time-select v-model="workTime.day1" class="inputWidth"  :editable='false'
                        :picker-options="{
                          start: '00:00',
                          step: '00:30',
                          end: '59:59'
                        }">   
                       </el-time-select>
               <span class="tip">(提示：输入格式为 xx:xx )</span>         
             </div>
             <div v-if="timeRadio==2" >
               执行时间  <el-time-picker class="inputWidth"
                        v-model="workTime.day2"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
               <span class="tip">(提示：输入格式为 xx:xx:xx)</span>         
             </div>
             <div v-if="timeRadio==3" >
               <div>
                 <el-radio-group v-model="weekRadio">
                  <el-radio  label="MON" border size="mini">周一</el-radio>
                  <el-radio  label="TUE" border size="mini">周二</el-radio>
                  <el-radio  label="WED" border size="mini">周三</el-radio>
                  <el-radio  label="THU" border size="mini">周四</el-radio>
                  <el-radio  label="FRI" border size="mini">周五</el-radio>
                  <el-radio  label="SAT" border size="mini">周六</el-radio>
                  <el-radio  label="SUN" border size="mini">周日</el-radio>
                </el-radio-group>
              </div>
               <div style="margin-top:40px">执行时间  <el-time-picker class="inputWidth"
                        v-model="workTime.day3"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
                      <span class="tip">(提示：输入格式为 xx:xx:xx)</span>     
               </div>
             </div>
             <div v-if="timeRadio==4" >
               执行时间  
              <el-input-number style="width:100px" v-model="dayNum" controls-position="right" :min="1" :max="31"></el-input-number>号
               <el-time-picker class="inputWidth"
                        v-model="workTime.day4"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
               <span class="tip">(提示：输入格式为 xx:xx xx:xx:xx)</span>         
             </div>
             <div v-if="timeRadio==5" >
               执行时间  
              <el-input-number 
              style="width:100px" 
              v-model="monthNum" 
              controls-position="right" 
              readonly
              :min="1" :max="12"
              >
              </el-input-number>月
              <el-input-number 
              style="width:100px" 
              v-model="month_day_Num" 
              controls-position="right" 
              :min="1" :max="maxday"
              @change="changeDay"
              @focus="changeDay">
              </el-input-number>
              日
                <el-time-picker class="inputWidth"
                        v-model="workTime.day5"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
              <div class="tip mar_top_12">(提示：输入格式为 xxxx:xx:xx xx:xx:xx)</div>   
             </div>
          </div>
        </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialogInner()">取 消</el-button>
        <el-button type="primary"  @click="sureChooseTime(1)">确 定</el-button>
      </div>
      </el-dialog>
      <el-form :model="addInfo" label-width="120px" :rules="rules" ref="addInfo" :inline="true" :label-position="'right'">
        <el-form-item label="任务名称"   prop="jobName">
          <el-input v-model="addInfo.jobName" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="任务描述"   prop="description">
          <el-input v-model="addInfo.description" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="服务ID"   prop="serviceId">
          <el-input v-model="addInfo.serviceId" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="服务调用地址"   prop="url">
          <el-input v-model="addInfo.url" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="时间表达式"  prop="cron">
            <el-input v-model="addInfo.cron"    @focus="openTimeChooseAdd" readonly class="inputWidth"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">取 消</el-button>
        <el-button type="primary"  @click="addSure('addInfo')">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="修改任务" :visible.sync="dialogEdit" :close-on-click-modal="false">
      <el-dialog width="45%" title="时间表达式设置" :visible.sync="innerVisibleEdit" :close-on-click-modal="false" append-to-body>
        <div>
          <div>
            <el-radio-group v-model="timeRadio">
                <el-radio  :label="0" border>每分钟</el-radio>
                <el-radio  :label="1" border>每小时</el-radio>
                <el-radio  :label="2" border>每天</el-radio>
                <el-radio  :label="3" border>每周</el-radio>
                <el-radio  :label="4" border>每月</el-radio>
                <el-radio  :label="5" border>每年</el-radio>
              </el-radio-group>
          </div>
          <div style="margin-top:40px">
             <div v-if="timeRadio==0" >
               执行时间  <el-input-number 
                        style="width:100px" 
                        v-model="workTime.day0" 
                        controls-position="right" 
                        :min="1" :max="60"
                        >
                        </el-input-number>
               <!-- <el-input v-model="workTime.day0" clearable  class="inputWidth"/> -->
               <span style="color:red;margin-left:10px">(提示：每隔几分钟执行一次，即输入几)</span>
             </div>
             <div v-if="timeRadio==1" >
               执行时间  <el-time-select v-model="workTime.day1" class="inputWidth"  :editable='false'
                        :picker-options="{
                          start: '00:00',
                          step: '00:30',
                          end: '59:59'
                        }">   
                       </el-time-select>
               <span class="tip">(提示：输入格式为 xx:xx )</span>         
             </div>
             <div v-if="timeRadio==2" >
               执行时间  <el-time-picker class="inputWidth"
                        v-model="workTime.day2"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
               <span class="tip">(提示：输入格式为 xx:xx:xx)</span>         
             </div>
             <div v-if="timeRadio==3" >
               <div>
                 <el-radio-group v-model="weekRadio">
                  <el-radio  label="MON" border size="mini">周一</el-radio>
                  <el-radio  label="TUE" border size="mini">周二</el-radio>
                  <el-radio  label="WED" border size="mini">周三</el-radio>
                  <el-radio  label="THU" border size="mini">周四</el-radio>
                  <el-radio  label="FRI" border size="mini">周五</el-radio>
                  <el-radio  label="SAT" border size="mini">周六</el-radio>
                  <el-radio  label="SUN" border size="mini">周日</el-radio>
                </el-radio-group>
              </div>
               <div style="margin-top:40px">执行时间  <el-time-picker class="inputWidth"
                        v-model="workTime.day3"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
                      <span class="tip">(提示：输入格式为 xx:xx:xx)</span>     
               </div>
             </div>
             <div v-if="timeRadio==4" >
               执行时间  
              <el-input-number style="width:100px" v-model="dayNum" controls-position="right" :min="1" :max="31"></el-input-number>号
               <el-time-picker class="inputWidth"
                        v-model="workTime.day4"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
               <span class="tip">(提示：输入格式为 xx:xx xx:xx:xx)</span>         
             </div>
             <div v-if="timeRadio==5" >
               执行时间  
              <el-input-number 
              style="width:100px" 
              v-model="monthNum" 
              controls-position="right" 
              readonly
              :min="1" :max="12"
              >
              </el-input-number>月
              <el-input-number 
              style="width:100px" 
              v-model="month_day_Num" 
              controls-position="right" 
              :min="1" :max="maxday"
              @change="changeDay"
              @focus="changeDay">
              </el-input-number>
              日
                <el-time-picker class="inputWidth"
                        v-model="workTime.day5"
                        arrow-control
                        :editable='false'
                        :picker-options="{
                          selectableRange: '00:00:00 - 23:59:59'
                        }"
                      >
                      </el-time-picker> 
              <div class="tip mar_top_12">(提示：输入格式为 xxxx:xx:xx xx:xx:xx)</div>   
             </div>
          </div>
        </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialogInner()">取 消</el-button>
        <el-button type="primary"  @click="sureChooseTime(2)">确 定</el-button>
      </div>
      </el-dialog>
      <el-form :model="editInfo" label-width="120px" :rules="rules" ref="editInfo" :inline="true" :label-position="'right'">
       <el-form-item label="任务名称"   prop="jobName">
          <el-input v-model="editInfo.jobName" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="任务描述"   prop="description">
          <el-input v-model="editInfo.description" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="服务ID"   prop="serviceId">
          <el-input v-model="editInfo.serviceId" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="服务调用地址"   prop="url">
          <el-input v-model="editInfo.url" clearable class="inputWidth" ></el-input>
        </el-form-item>
        <el-form-item label="时间表达式"  prop="cron">
            <el-input v-model="editInfo.cron"    @focus="openTimeChooseEdit" readonly class="inputWidth"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">取 消</el-button>
        <el-button type="primary"  @click="editSure('editInfo')">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="查看执行记录" :visible.sync="dialogFind" width="70%" :close-on-click-modal="false">
        <div>
         <el-table
          :data="historyData"
          border
          stripe
          height="440"
          style="width: 100%"
           ref="multipleTable">
          <el-table-column prop="jobName" label="任务名称">
          </el-table-column>
          <el-table-column
            label="开始时间"
          >
           <template slot-scope="scope">
            {{scope.row.startTime | timetrans}}
          </template>
          </el-table-column>
          <el-table-column
            label="完成时间"
          >
          <template slot-scope="scope">
            {{scope.row.completeTime | timetrans}}
          </template>
          </el-table-column>
          <el-table-column
            prop="failureCause"
            label="失败原因"
            >
          </el-table-column>
          <el-table-column
            prop="remoteUrl"
            label="调用的url"
            >
          </el-table-column>
          <el-table-column
            prop="resultMsg"
            label="返回的消息"
            >
          </el-table-column>
        </el-table>
        <div class="pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pageNum"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="dataSize">
          </el-pagination>
        </div>
    </div>
    </el-dialog>
   </div>
  </template>

<script>
export default {
  data() {
    //表单验证飞控去空格后非空
    var validatePass = (rule, value, callback) => {
      if ( value.replace(/(^\s*)|(\s*$)/g, "") === '') {//前后去空格
        callback(new Error('请输入必填项'));
      }else {
        callback();
      }
    };
    return {
      dataSize: 0, //总条数//执行历史记录
      tableData: [],
      pageNum: 1,//执行历史记录
      pageSize: 10,//执行历史记录
      historyData: [],//执行历史记录
      formData:{},//查询条件传值
      menuButtonList:[],//菜单按钮列表
      dialogAdd: false,//新增框默认隐藏
      dialogEdit: false,//修改框默认隐藏
      dialogFind:false,//查看执行记录
      innerVisibleAdd:false,//新增-时间选择弹出
      innerVisibleEdit:false,//修改-时间选择
      timeRadio:2,//时间表达式设置
      weekRadio:"MON",//星期几单选 默认周一
      workTime:{
        day0:'',
        day1:'',
        day2:'',
        day3:'',
        day4:'',
        day5:'',
      },//选择的具体日期值
      dayNum:"1",//每月几号
      monthNum:"",//每年几月
      month_day_Num:"",//每年几月的几号
      maxday:31,//每月最多天数
      getDataUrl: this.$store.state.url+'job/listJobs',//获取表格数据
      addUrl: this.$store.state.url+'job/addJob',//新增
      editUrl: this.$store.state.url+'job/updateCron',//修改
      stopUrl: this.$store.state.url+'job/pauseJob',//停用
      startUrl: this.$store.state.url+'job/resumeJob',//启用
      delUrl: this.$store.state.url+'job/removeJob',//作废
      getHistoryData: this.$store.state.url+'job/listJobExecutionLog',//作废
      formInline: {//快捷查询
          jobName: '',
      },
      addInfo:{
          jobName:'',//任务名称
          description:'',//任务描述
          serviceId:'',//服务id
          cron:'',//时间表达式
          url:'',//服务调用url
      //    sync:true,//是否允许同步执行
          //runStatus:true,//启用状态
      },
      editInfo:{},
      editInfoBefore:{},//修改前的值 取消修改用
      rules: {//表单验证
        jobName: [
          { required: true, validator: validatePass, trigger: 'blur' },
          ],
        serviceId: [
          { required: true, validator: validatePass, trigger: 'blur' },
          ],
        url: [
          { required: true, validator: validatePass, trigger: 'blur' },
          ],
        cron: [
          { required: true, validator: validatePass, trigger: 'change' },
          ],
      },
   };  
  },
  watch: {
    pageNum: function (){
     this.getHistory()
      },
    pageSize: function (){
     this.getHistory()
    },
  },
  mounted: function () {
      this.$nextTick(function () {
        this.getData();
     //   this.getHistory();
        this.getButton();//获取页面按钮
  })
  },
  methods: {
    //获取页面按钮
    getButton(){
       this.menuCode=this.$store.state.menuCode;//防止按钮下面还有权限 切换菜单时值会改变
       var params = new URLSearchParams();
        params.append('USER_NAME', localStorage.getItem('ms_username'));
        params.append('MENU_CODE', this.menuCode);
        params.append('BUTTON_CODE', '');
        this.$axios.post(this.$store.state.getButtonUrl, params).then(res =>  {
        if(0==res.data.code){//设置成功
          this.menuButtonList=res.data.data;
        }else{
          this.$message({
            showClose: true,
            message: res.data.msg,
            type: 'error'
          });
        }
        })
    },
    //判断点击哪个按钮
    chooseClick(method){
        if('addJob'==method){
          this.addJob('addInfo');
        }else if('editJob'==method){
          this.editJob();
        }else if('stopJob'==method){
          this.stopJob();
        }else if('starJob'==method){
          this.starJob();
        }else if('delJob'==method){
          this.delJob();
        }else if('findHistory'==method){
          this.findHistory();
        }
    },
     //改变每页条数
      handleSizeChange(val) {
        this.pageSize = val;
      },
      //改变页数
      handleCurrentChange(val) {
        this.pageNum = val;
      },
     //查询    
    searchForm(){
      this.getData();
    },
    //选中一条
    chooseOne(val) {
      this.editInfoBefore=JSON.parse(JSON.stringify(val));
    },
    //每月多少最多几天根据月份来判断
    changeDay(){
      if(this.monthNum%2 ==0){
        this.maxday=30
      }else{
        this.maxday=31
      }
      if(2==this.monthNum){//默认二月28天
        this.maxday=28
      }
      if(8==this.monthNum){
        this.maxday=31
      }
    }, 
    //选好时间
    sureChooseTime(val){
      var time;
      var cron;
      if(0==this.timeRadio){//每分钟执行
        time=this.workTime.day0;
        if(undefined!=time){
          cron="0 0/"+time+" * * * ?";
        }else{
          this.$message({
          type: 'error',
          message: '请填写执行时间!'
        });
        return;
        }
      }else if(1==this.timeRadio){//每小时
        time=this.workTime.day1;
         if(""!=time&&null!=time){
           var minute=time.substr(0,1)=="0"?time.substr(1,1):time.substr(0,2);
           var second=time.substr(3,2)=="00"?"0":time.substr(3,2);
           cron= second+" "+minute+" "+"*/1  * * ?";
        }else{
          this.$message({
          type: 'error',
          message: '请填写执行时间!'
        });
        return;
        }
      }else if(2==this.timeRadio){//每天
        time=this.workTime.day2
        if(""!=time&&null!=time){
          cron=time.getSeconds()+" "+time.getMinutes()+" "+time.getHours()+" * * ?"
        }else{
          this.$message({
          type: 'error',
          message: '请填写执行时间!'
        });
        return;
        }
      }else if(3==this.timeRadio){//每周
       time=this.workTime.day3
        if(""!=time&&null!=time){
           cron=time.getSeconds()+" "+time.getMinutes()+" "+time.getHours()+" ?"+" * "+this.weekRadio
        }else{
          this.$message({
          type: 'error',
          message: '请填写执行时间!'
          });
        return;
        }
      }else if(4==this.timeRadio){//每月
        time=this.workTime.day4
        if(""!=time&&null!=time&&undefined!=this.dayNum){
           cron=time.getSeconds()+" "+time.getMinutes()+" "+time.getHours()+" "+this.dayNum+" * ?"
        }else{
          this.$message({
          type: 'error',
          message: '请填写执行时间!'
          });
        return;
        }
      }else if(5==this.timeRadio){//每年
         time=this.workTime.day5
         if(""!=time&&null!=time&&undefined!=this.month_day_Num&&undefined!=this.monthNum){
          cron=time.getSeconds()+" "+time.getMinutes()+" "+time.getHours()+" "+this.month_day_Num+" "+this.monthNum+" * ?"
          }else{
            this.$message({
            type: 'error',
            message: '请填写执行时间!'
            });
          return;
          }
      }
      if(1==val){//新增
        this.innerVisibleAdd = false; 
        this.addInfo.cron=cron;
      }else{//修改
         this.innerVisibleEdit = false; 
        this.editInfo.cron=cron;
      }
    },
    //重置查询域
    resetForm(formInline){
       this.$refs[formInline].resetFields();
    },
    //用户新增   
    addJob(addInfo){
      this.dialogAdd = true;
      if(this.$refs[addInfo]){//清空表单
        this.$refs[addInfo].resetFields();
       }
    },
    //选择时间表达式-新增
    openTimeChooseAdd(){
      this.innerVisibleAdd=true;
    },
    //选择时间表达式-修改
    openTimeChooseEdit(){
      this.innerVisibleEdit=true;
    },
    //确认新增
    addSure(formName){
       this.$refs[formName].validate((valid) => {
          if (valid) {
              var params = new URLSearchParams();
              params.append('jobName', this.addInfo.jobName);
              params.append('cron', this.addInfo.cron);
              params.append('serviceId', this.addInfo.serviceId);
              params.append('url', this.addInfo.url);
              params.append('description', this.addInfo.description);
              this.$axios.post(this.addUrl,params).then(res =>  {
                if(0==res.data.code){//新增成功
                  this.getData();
                  this.$message({
                    showClose: true,
                    message: '新增定时任务成功',
                    type: 'success'
                  });
                  this.dialogAdd = false;//隐藏dialo  
                }else{
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
    //取消新增，修改，
    cancelDialog(){
      this.dialogAdd = false;//隐藏新增dialo  
      this.dialogEdit = false;//修改dialo  
      this.dialogFind = false;//隐藏查看执行记录  
      //this.editInfo=JSON.parse(JSON.stringify(this.editInfoBefore))//回到修改前的值
    },
    //取消选择时间
    cancelDialogInner(){
        this.innerVisibleAdd = false; 
        this.innerVisibleEdit = false; 
    },
    //修改信息
    editJob(){
      if(this.editInfoBefore){
       if(this.editInfoBefore.jobName){
          this.dialogEdit = true;
          this.editInfo=JSON.parse(JSON.stringify(this.editInfoBefore))//回到修改前的值
        }else{
          this.$message({
            showClose: true,
            message: "请选择一条数据进行修改",
            type: 'error'
          });
        }
       }else{
          this.$message({
            showClose: true,
            message: "请选择一条数据进行修改",
            type: 'error'
          });
        }
    },
    //确认修改
    editSure(formName){
       this.$refs[formName].validate((valid) => {
          if (valid) {
            var params = new URLSearchParams();
            params.append('jobId', this.editInfoBefore.id);
            params.append('jobName', this.editInfo.jobName);
            params.append('cron', this.editInfo.cron);
            params.append('serviceId', this.editInfo.serviceId);
            params.append('url', this.editInfo.url);
            params.append('description', this.editInfo.description);
            this.$axios.post(this.editUrl,params).then(res =>  {
              if(0==res.data.code){//修改成功
                this.getData();
                this.$message({
                    showClose: true,
                    message: '修改用户成功',
                    type: 'success'
                  });
                this.dialogEdit = false;//隐藏dialo 
              }else{
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
    //停用   
    stopJob(){
     if(this.editInfoBefore){
      if(this.editInfoBefore.id){
          this.$confirm('此操作将停用该定时任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios.get(this.stopUrl+'?jobId='+this.editInfoBefore.id).then(res =>  {
          if(0==res.data.code){
            this.getData();
            this.$message({
            type: 'success',
            message: '停用成功!'
          });
          }else{
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
            message: '已取消操作'
          });          
        });
        }else{
          this.$message({
            showClose: true,
            message: "请选择一条数据进行操作",
            type: 'error'
          });
        }
     }else{
          this.$message({
            showClose: true,
            message: "请选择一条数据进行操作",
            type: 'error'
          });
        }
    },
    //作废 
    delJob(){
      if(this.editInfoBefore){
       if(this.editInfoBefore.id){
          this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios.get(this.delUrl+'?jobId='+this.editInfoBefore.id).then(res =>  {
          if(0==res.data.code){//删除成功
            //还剩的条数>当前页数减一乘每页条数且 当前页数不是第一页
            this.getData();
            //this.editInfo={};
          //  this.editInfoBefore={};
            this.$message({
            type: 'success',
            message: '删除成功!'
          });
          }else{
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
            message: '已取消删除'
          });          
        });
        }else{
          this.$message({
            showClose: true,
            message: "请选择一条数据进行删除",
            type: 'error'
          });
        }
      }else{
      this.$message({
        showClose: true,
        message: "请选择一条数据进行删除",
        type: 'error'
      });
     }
    },
    //启用
    starJob(){
      if(this.editInfoBefore){
      if(this.editInfoBefore.id){
          this.$confirm('此操作将启用该定时任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios.get(this.startUrl+'?jobId='+this.editInfoBefore.id).then(res =>  {
          if(0==res.data.code){//成功
            this.getData();
           // this.editInfo={};
            this.editInfoBefore={};
            this.$message({
            type: 'success',
            message: '启用成功!'
          });
          }else{
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
            message: '已取消操作'
          });          
        });
        }else{
          this.$message({
            showClose: true,
            message: "请选择一条数据进行操作",
            type: 'error'
          });
         }
      }else{
          this.$message({
            showClose: true,
            message: "请选择一条数据进行操作",
            type: 'error'
          });
         }
    },
    //打开查看历史记录 dilog
    findHistory(){
     this.dialogFind = true;  
     this.getHistory();
    },
    //获取历史记录
    getHistory(){
      this.$axios.get(this.getHistoryData+'?pageSize='+this.pageSize+'&pageNum='+this.pageNum).then(res =>  {
       if(0==res.data.code){//查询成功
        this.historyData=res.data.data.list;
        this.dataSize=res.data.data.total;
       }else{
         this.$message({
          showClose: true,
          message: res.data.msg,
          type: 'error'
        });
       }
      })
    },
    getData() {
      this.$axios.get(this.getDataUrl+'?jobName='+this.formInline.jobName).then(res =>  {
       if(0==res.data.code){//查询成功
        this.tableData=res.data.data;
        for(var i=0;i<this.tableData.length;i++){
            if(1==this.tableData[i].status){
                this.tableData[i].status='运行中'
            }else{
                this.tableData[i].status='已停用'
            }
        }
       }else{
         this.$message({
          showClose: true,
          message: res.data.msg,
          type: 'error'
        });
       }
      })
    },
  },
  filters: {
    timetrans: function (value) {
      value=new Date(value);
      var Y = value.getFullYear() + '-';
      var M = (value.getMonth()+1 < 10 ? '0'+(value.getMonth()+1) : value.getMonth()+1) + '-';
      var D = (value.getDate() < 10 ? '0' + (value.getDate()) : value.getDate()) + ' ';
      var h = (value.getHours() < 10 ? '0' + value.getHours() : value.getHours()) + ':';
      var m = (value.getMinutes() <10 ? '0' + value.getMinutes() : value.getMinutes()) + ':';
      var s = (value.getSeconds() <10 ? '0' + value.getSeconds() : value.getSeconds());
      return Y+M+D+h+m+s;
    }
  }
};
</script>

<style scoped>
.handle-box {
  margin-bottom: 20px;
}
.inputWidth{
   max-width:200px
}
.mar_top_12{
  margin-top:12px
}
.roleStyle{
 width:180px;
 height:35px;
 line-height:35px;
 float:left;
 text-align:center;
 border:1px solid #d1dbe5;
}
.topNoStyle{
  border-top:none
}
.rightNoStyle{
  border-right:none
}
.tdStyle{
  width:180px;
  height:40px;
  line-height:40px;
  text-align:center;
  border:1px solid #d1dbe5;
  border-top:none;
  border-right:none
}
.tip{
  color:red;
  margin-left:10px
}
</style>