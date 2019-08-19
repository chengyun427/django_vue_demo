<template>
  <div class="login-wrap">
    <!-- <div class="ms-title">后台管理系统</div> -->
    <div class="ms-conter">
      <div class="ms-logo"></div>
      <el-button type="primary" class="login" @click="submitLogin('ruleForm')">登录</el-button>
      <el-button type="primary" class="register">注册</el-button>
    </div>
    <!-- <div class="ms-login"> -->
    <!-- <span @click="close()">
        <i class="el-icon-close"></i>
    </span>-->

    <el-dialog width="100%" :visible.sync="login" :close-on-click-modal="false" class="ms-login" top="0px">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="0px"
        class="demo-ruleForm"
      >
        <el-form-item prop="username">
          <el-input v-model="ruleForm.username" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" placeholder="密码" v-model="ruleForm.password"></el-input>
        </el-form-item>
        <!-- <el-form-item prop="code">
                    <el-input class="code-width" placeholder="验证码" v-model="ruleForm.validateCode" @keyup.enter.native="submitForm('ruleForm')"></el-input>
                    <img v-bind:src="imgUrl" @click="getValidateCode" class="code-img-width">
        </el-form-item>-->
        <div class="login-btn">
          <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
        </div>
      </el-form>
    </el-dialog>

    <!-- </div> -->
  </div>
</template>
<script>
export default {
  data: function() {
    return {
      deviceId: "", //设备id
      imgUrl: "", //图片路径
      ruleForm: {
        username: "",
        password: ""
      },
      loginUrl:
        this.$store.state.url + "api/getUserByLogin", //登陆
      loading: "", //加载遮罩
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" }
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      },
      login: false
    };
  },
  mounted: function() {
    //this.getValidateCode();
  },
  methods: {
    submitLogin(ruleForm) {
      this.login = true;
    },
    submitForm(formName) {
      this.$store.state.options = [];
      this.openFullScreen();
      const self = this;
      self.$refs[formName].validate(valid => {
        if (valid) {
          let params = new URLSearchParams();
          params.append("userAccount", this.ruleForm.username);
          params.append("userPwd", this.ruleForm.password);
          this.$axios
            .get(
              this.loginUrl +
                "?userAccount=" +
                this.ruleForm.username +
                "&userPwd=" +
                this.ruleForm.password
            )
            .then(res => {
              this.loading.close(); //关闭加载
              if (0 == res.data.code) {
                //登陆成功
                sessionStorage.setItem("access_token", res.data.data);
                localStorage.setItem("ms_username", this.ruleForm.username);
                this.$router.push("/home");
              } else {
                this.$message({
                  type: "error",
                  message: res.data.msg
                });
                this.ruleForm.password = "";
                this.ruleForm.validateCode = "";
              }
            });
        } else {
          this.loading.close(); //关闭加载
          return false;
        }
      });
    },
    //打开加载
    openFullScreen() {
      this.loading = this.$loading({
        lock: true,
        text: "登录中...",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)"
      });
    },
    // 获取验证码
    getValidateCode() {
      this.$axios.post(this.validateCodeUrl).then(res => {
        if (0 == res.data.code) {
          //成功
          var data = res.data.data;
          this.deviceId = data.deviceId;
          this.imgUrl = "data:image/jpg;base64," + data.image;
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
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url("../../assets/img/login/loginBG.jpg");
  background-size: 100% 100%;
}
.ms-title {
  position: absolute;
  top: 50%;
  width: 100%;
  margin-top: -230px;
  text-align: center;
  font-size: 30px;
  color: #fff;
}
.ms-conter {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 420px;
  height: 200px;
  margin-left: -195px;
  margin-top: -40px;
}
.ms-conter .register {
  margin: 0 15px;
  height: 30px;
  width: 186px;
  color: #fff;
  border-width: 1px;
  border-style: solid;
  background: rgba(0, 0, 0, 0.2);
  border-color: #ffffff;
}
.ms-conter .login {
  height: 30px;
  width: 186px;
}
.ms-logo {
  margin-bottom: 10px;
  height: 88px;
  width: 420px;
  background-position: -14px 0;
  background-size: 100% 100%;
  background-image: url("../../assets/img/login/loginIMG.png");
  background-repeat: no-repeat;
  animation: move 1s;
}
@keyframes move {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 300px;
  height: 200px;
  margin: -150px 0 0 -190px;
  padding: 40px;
  border-radius: 5px;
}
.el-dialog__wrapper {
  overflow: hidden;
}
.login-btn {
  text-align: center;
}
.login-btn button {
  width: 100%;
  height: 36px;
}
.code-width {
  width: 50%;
}
.code-img-width {
  width: 40%;
  margin-left: 5%;
  vertical-align: middle;
}
</style>
