<template>
    <el-col :span="18" style="float:right; margin-right:170px" id="log">
        <div class="title">
            <span>
                <p class="el-icon-tickets" style="font-size: 25px"></p> Server Log
            </span>
            <span>
                <p class="el-icon-delete"
                @click="clear_log()" 
                style="font-size: 25px; float:right; margin-right:30px"></p> 
            </span>
        </div>
        <el-card 
        class="box-card" 
        style="margin-left:40px; padding:0px"
        :data="logs"
        id="logs"
        >
          <div v-for="log in logs" :key="log" class="text item">
            {{ log }}
            </div>
        </el-card>
    </el-col>
</template>

<script>
import moment from 'moment'

export default {   
    data(){
        return{
            logs : [],
        }
    },
    methods:{
        add_log(args){
            var log = ''
            var block = args[0]
            var msg = args[1]
            if(block == 0){
                log = " [UPLOAD] " + msg 
            }
            else if(block == 1){
                log = " [DETECT] " + msg
            }
            else if(block == 2){
                log = " [CODE] " + msg
            }
            else if(block == 3){
                log = " [TRANSMIT] " + msg
            }
            var time = new Date().getTime()
            time  =  moment(time).format('YYYY-MM-DD HH:mm:ss')
            log = time.toString() + log
            this.logs.push(log)
        },
        clear_log(){
            this.logs = []
        }
    },
}
</script>
<style scoped>
.title{
    color: #656d6d; 
    font-weight: bold; 
    margin-left: 40px;
    height:65px;
    width: 100%;
    background: -webkit-linear-gradient(bottom,hsla(0,0%,59%,.15),hsla(0,0%,59%,0),white) no-repeat;
}
  .text {
    font-size: 15px;
    color: #656d6d;
  }

  .item {
    padding: 6px 0;
  }

  .box-card {
    width: 100%;
  }
</style>