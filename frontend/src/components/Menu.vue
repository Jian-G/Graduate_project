<template>
<el-col :span="3" style="margin-left:10px">
    <el-menu
      default-active=""
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      background-color="#ABB1B3"
      text-color="#fff"
      active-text-color="#ffd04b"
      style=";margin-top:20px">
      <el-menu-item index="0" @click="scroll(0)" style="text-align:center;font-size:18px">
        <span slot="title" >Menu</span>
      </el-menu-item>
      <el-menu-item index="1" @click="scroll(1)">
        <i class="el-icon-upload"></i>
        <span slot="title">Upload Video</span>
      </el-menu-item>
      <el-menu-item index="2" @click="scroll(2)">
        <i class="el-icon-menu"></i>
        <span slot="title">Detect Result</span>
      </el-menu-item>
      <el-menu-item index="3" @click="scroll(3)">
        <i class="el-icon-document"></i>
        <span slot="title">Code Detail</span>
      </el-menu-item>
      <el-menu-item index="4" @click="scroll(4)">
        <i class="el-icon-s-promotion"></i>
        <span slot="title">Transmission Info</span>
      </el-menu-item>
        <el-menu-item index="5" @click="scroll(5)">
        <i class="el-icon-tickets"></i>
        <span slot="title">Server Log</span>
      </el-menu-item>
    </el-menu>
  <router-view></router-view>

</el-col>
</template>
<script>
  export default {

    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
      scroll(id){
        if(id == 0)
          document.getElementById("Header").scrollIntoView();
        else if(id == 1)
          document.getElementById("upload").scrollIntoView();
        else if(id == 2)
          document.getElementById("detect").scrollIntoView();
        else if(id == 3)
          document.getElementById("code").scrollIntoView();
        else if(id == 4)
          document.getElementById("transmit").scrollIntoView();
        else if(id == 5)
        document.getElementById("log").scrollIntoView();
      }
    }
  }
</script>