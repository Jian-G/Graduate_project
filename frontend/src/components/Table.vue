<template>
    <el-col :span="18" style="float:right; margin-right:170px;" id="detect">
        <div class="title">
            <el-tooltip 
                class="item" 
                effect="dark" 
                content="This block shows detect result, you can preview!" 
                placement="right"
                >
            <span>
                <p class="el-icon-menu" style="font-size: 25px"></p> Detect Result
            </span>
            </el-tooltip>
        </div>
        <el-table 
            ref="detect" 
            :data="tabledata"
            stripe
            style="width: 100%; margin-left:40px; max-height:400px; overflow-y:auto"
            >
            <el-table-column type="index" label="Index" width="80" align="center"></el-table-column>
            <el-table-column prop="filename" label="FileName" width="400" align="center"></el-table-column>
            <el-table-column prop="filesize" label="FileSize(MB)" align="center"></el-table-column>
            <el-table-column prop="time" label="Time(S)" align="center"></el-table-column>
            <el-table-column label="Preview" align="center">
                <template slot-scope="scope">
                    <i class="el-icon-video-play" @click="play_video(scope.row.filename)"></i>
                </template>
            </el-table-column>
        </el-table>
            <video width="640" height="360" muted="muted" autoplay="autoplay" controls="controls"
            style="margin:30px 0 30px 250px" id="video">
                <source src="" type="video/mp4">
            </video>
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
                url: '/detect_result',
                data: this.tabledata
            })
            .then((response) => {
                var data = response.data.detect_result
                console.log(response.data.detect_result)
                for(i in data){
                    this.tabledata.push(data[i])
                    var msg = "Finish detect " + data[i]['filename']
                    this.$emit("add",1,msg)
                }
            })
            .catch((error) => {
                console.log(error)
            })
        },
        play_video(filename){
            var msg = "Preview " + filename
            document.getElementById("video").src = "http://localhost:5000/" + filename
            this.$emit("add",1,msg)
            console.log(document.getElementById("video").src)
        },
        start_timer(){
            this.timer = setInterval(()=>{
                    this.get_list()
                }, 3000 )
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