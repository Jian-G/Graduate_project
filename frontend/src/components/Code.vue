<template>
    <el-col :span="18" style="float:right; margin-right:170px" id="code">
        <div class="title">
            <el-tooltip 
                class="item" 
                effect="dark" 
                content="This block shows the encoded informations." 
                placement="right"
                >
                <span>
                    <p class="el-icon-document" style="font-size: 25px"></p> Code Detail
                </span>
            </el-tooltip>
        </div>
        <el-table 
            ref="file" 
            stripe
            :data="tabledata"
            style="width: 100%; margin-left:40px; max-height:400px; overflow-y:auto"
            >
            <el-table-column type="index" label="Index" width="80" align="center"></el-table-column>
            <el-table-column prop="filename" label="FileName" width="400" align="center"></el-table-column>
            <el-table-column prop="filesize" label="FileSize(MB)" align="center"></el-table-column>
            <el-table-column prop="blocks" label="Blocks" align="center"></el-table-column>
            <el-table-column prop="drops" label="Drops" align="center"></el-table-column>
            <el-table-column label="Redundancy" width="120" align="center">1.2</el-table-column>
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
                url: '/file_list',
                data: this.tabledata
            })
            .then((response) => {
                var data = response.data.file_list
                for(i in data){
                    this.tabledata.push(data[i])
                    var msg = "File " + data[i]['filename'] + " has been encoded"
                    this.$emit("add",2,msg)
                }
            })
            .catch((error) => {
                console.log(error)
            })
        },
        play_video(filename){
            console.log(filename)
        },
        start_timer(){
            this.timer = setInterval(()=>{
                    this.get_list()
                }, 3000)
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
.line{
  /* float:right; */
  height: 1px;
  margin:auto;
  background:#d4c4c4;
  position: relative;
  text-align: center;
}
</style>