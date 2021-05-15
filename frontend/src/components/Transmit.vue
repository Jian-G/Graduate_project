<template>
    <el-col :span="18" style="float:right; margin-right:170px" id="transmit">
        <div class="title">
             <el-tooltip 
                class="item" 
                effect="dark" 
                content="This block shows the transmit informations." 
                placement="right"
                >
                <span>
                    <p class="el-icon-s-promotion" style="font-size: 25px"></p> Transmission Info
                </span>
                </el-tooltip>
        </div>
        <el-table 
            ref="detect" 
            :data="tabledata"
            stripe
            style="width: 100%; margin-left:40px; max-height:400px; overflow-y:auto"
            >
            <el-table-column prop="host" label="Host" width="150" align="center"></el-table-column>
            <el-table-column prop="port" label="Port"  width="150" align="center"></el-table-column>
            <el-table-column prop="filename" label="Filename" width="250" align="center"></el-table-column>
            <el-table-column prop="state" label="States" align="center"></el-table-column>
            <el-table-column prop="info" label="Received/Need/Total" width="300" align="center"></el-table-column>
        </el-table>
    </el-col>
</template>

<script>
export default {   
    data(){
        return{
            tabledata : [],
        }
    },
    methods:{
        get_list: function(i) {
            this.axios({
                method: 'post',
                url: '/transmit_info',
            })
            .then((response) => {
                console.log(response.data.transmit_info)
                var newdata = response.data.transmit_info
                var flag = false
                for(var i in newdata){
                    flag = false
                    for(var j in this.tabledata){
                        if(newdata[i]['filename'] == this.tabledata[j]['filename']){
                            flag = true
                            if(newdata[i]['state'] != this.tabledata[j]['state']){
                                var msg = newdata[i]['filename'] + " is " + newdata[i]['state'] + " to " + newdata[i]['host'] + ":" + newdata[i]['port']
                                this.$emit("add",3,msg)
                            }
                        }
                    }
                    if(flag == false){
                        var msg = newdata[i]['filename'] + " is " + newdata[i]['state'] + " to " + newdata[i]['host'] + ":" + newdata[i]['port']
                        this.$emit("add",3,msg)
                    }
                }
                this.tabledata = newdata
            })
            .catch((error) => {
                console.log(error)
            })
        },
        start_timer(){
            this.timer = setInterval(()=>{
                    this.get_list()
                }, 1500 )
        },
    },
    created(){
        this.start_timer()
        // this.get_list()
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
</style>