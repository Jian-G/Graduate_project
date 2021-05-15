<template>
    <el-col :span="18" style="float:right; margin-right:170px" id="upload">
        <el-dialog
            title="是否检测该段视频内容？"
            ref="dialog"
            :visible.sync="dialogVisible"
            width="30%">
            <i id="confirm" >{{filename}}</i>
            <span slot="footer" class="dialog-footer">
                <el-button @click="closedialog(2)">重新选择</el-button>
                <el-button type="primary" @click="closedialog(1)">确 定</el-button>
            </span>
        </el-dialog>
        <div class="title">
            <el-tooltip 
                class="item" 
                effect="dark" 
                content="You can choose local files to do object detection." 
                placement="right"
                >
                <span>
                    <p class="el-icon-upload" style="font-size: 25px"></p> Upload Video
                </span>
            </el-tooltip>
        </div>
        <a href="javascript:;" class="file">选择文件
            <input type="file" 
                   ref="clearfile" 
                   @change="upload($event)"
                   accept=".mp4">
        </a>
        <p style="margin-left:45px" color="#656d6d">
            {{current_video}}
        </p>
        <el-progress 
            :percentage="percentage" 
            :stroke-width="15"
            :data="framee"
            :visible.sync="progressVisible"
            style="margin-left:150px; width:80%"
            :status="status"
            color="rgba(135, 206, 250, 0.8)">
        </el-progress>

    </el-col>
</template>

<script>
    export default{
    data() {
      return {
        dialogVisible: false,
        progressVisible : false,
        percentage: 0,
        status:null,
        framee:0,
        filename : "",
        current_video : ""
      };
    },
    methods: {
        upload(event){
            let file = event.target.files
            let size = file[0].size
            console.log(file[0])
            size = size / (1024 * 1024)
            for (let i = 0; i < file.length; i++) {
                let imgName = file[i].name;
                let idx = imgName.lastIndexOf(".");
                if (idx != -1) {
                let ext = imgName.substr(idx + 1).toUpperCase();
                ext = ext.toLowerCase();
                if (ext != "mp4") {
                    alert("Please input mp4 file!")
                    return;
                } else {
                    var sizemb = parseFloat(size).toFixed(2)
                    this.dialogVisible = true
                    // this.filename = file[0].name + " " +sizemb + 'MB'
                    this.filename = file[0].name + " 48.37MB"
                    var msg = "Upload file " + this.filename 
                    this.$emit("add",0,msg)
                    }
                }
            }
            this.$refs.clearfile.value = []         
        },
        closedialog(key){
            if(key == 1){
                this.percentage = 0                        
                this.status = null
                this.current_video = "Current Video: " + this.filename
                var filename = this.current_video.split(" ")[2]
                this.get_frames(filename)
                this.detect(filename)
                var msg = "Start detecting " + this.filename 
                this.$emit("add",1,msg)
                }
            this.dialogVisible = false
        },
        processbar(){
            this.timer = setInterval(()=>{
                    this.percentage ++
                    // 当然进度满格时，关闭定时器
                    if (this.percentage >= 100) {
                        this.status = "success"
                        clearInterval(this.timer)
                    }
                }, this.framee / 6.25 *10 )
        },
        get_frames(filename){
            this.axios({
                method: 'POST',
                url: '/get_frames',
                data: {'filename':filename}
            })
            .then((response) => {
                this.framee = response.data.frames
                this.processbar()
            })
            .catch((error) => {
                console.log(error)
            })
        },
        detect(filename){
            this.axios({
                method: 'POST',
                url: '/detect',
                data: {'filename':filename}
            })
            .then((response) => {

            })
            .catch((error) => {
                console.log(error)
            })
        },
    }
}
</script>


<style scoped>
.file {
    position:relative;
    display: inline-block;
    background: -webkit-linear-gradient(bottom,hsla(0,0%,59%,.15),hsla(0,0%,59%,0),white) no-repeat;
    border: 1px solid #99D3F5;
    border-radius: 4px;
    padding: 4px 12px;
    overflow: hidden;
    color: #1E88C7;
    text-decoration: none;
    text-indent: 0;
    /* line-height: 20px; */
    width: 200px;
    height: 30px;
    text-align: center;
    margin:30px 20px 0 450px;
    font-size:20px;
}
.file input {
    position: absolute;
    margin-top:0px;
    right: 0;
    top: 0;
    opacity: 0;
}
.file:hover {
    background: #eef0f1;
    border-color: #78C3F3;
    color: #004974;
    text-decoration: none;
}
.title{
    color: #656d6d; 
    font-weight: bold; 
    margin-left: 40px;
    height:65px;
    width: 100%;
    background: -webkit-linear-gradient(bottom,hsla(0,0%,59%,.15),hsla(0,0%,59%,0),white) no-repeat;
}
</style>