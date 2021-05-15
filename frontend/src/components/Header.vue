<template>
  <div id="Header">
    <div class="top-left-edition">
      <span style="color: #21b3b9; font-weight: bold">
        <img  src="static/icon.jpeg" style="height:90px; width:90px"/>目标检测辅助下的视频高可靠回传系统
      </span>
    </div>
    <div class="top-right-edition">
        <span>key@bupt.edu.cn
          <i class="el-icon-user" style="font-size: 23px"></i>
        </span>
    </div>
  </div>
</template>
<script>
export default {
  name: "Header",
  data() {
    return {
      msg: "目标检测&视频回传",
      activeIndex: "1",
    };
  },
  methods: {},
};
</script>
<style scoped>
#Header {
  width: 92%;
  height: 80px;
  padding-top: 20px;
  margin-left: 60px;
  padding-bottom: 15px;
}

h1 {
  letter-spacing: 30px;
  font-size: 2.3em;
}
.top-left-edition span i {
  float: left;
  margin-right: 10px;
}
.top-right-edition span i {
  float: right;
  margin-right: 80px;
}

img,
input,
label {
  vertical-align: middle;
  padding-right: 70px;

}

.top-left-edition span {
  float: left;
  font-size: 25px;
  line-height: 24px;
}
.top-right-edition span {
  float: right;
  font-size: 20px;
  color: #999999;
  line-height: 24px;
  margin-left: 50px;
  margin-top:30px;
}
.line{
  width: 100%;
  height: 3px;
  background:#d4c4c4;
  text-align: center;
}
</style>


