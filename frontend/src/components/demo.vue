<template>
    <div class="demo">

      <!-- 新增修改按钮 -->
      <div class="handle-box">
        <el-button type="primary" icon="el-icon-setting" >测试</el-button>
        <!--<el-button type="primary" icon="el-icon-setting" @click="editAccount()">修改</el-button>-->
        <!--<el-button type="primary" icon="el-icon-setting" @click="EnableAccount()">启用</el-button>-->
        <!--<el-button type="primary" icon="el-icon-setting" @click="DisEnableAccount()">禁用</el-button>-->
      </div>
    </div>
</template>

<script>
    export default {
      name: "demo",
      data () {
        return {
          // msg: 'Welcome to Your Vue.js App',
          url: this.$store.state.url + 'api/testapi',//调用django接口地址
        }
      },
      mounted() {
        this.$axios.post(this.url,{"aa": 'bb'})
          .then((response) => {
            console.log(response)
            // console.log(response.data.main)
        })
      },

    }
</script>

<style scoped>

</style>
