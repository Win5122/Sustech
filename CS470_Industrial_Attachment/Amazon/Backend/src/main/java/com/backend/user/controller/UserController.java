package com.backend.user.controller;


import cn.dev33.satoken.annotation.SaCheckLogin;
import cn.dev33.satoken.annotation.SaCheckRole;
import cn.dev33.satoken.stp.StpUtil;
import com.backend.user.entity.User;
import com.backend.user.entity.dto.UserInfoDTO;
import com.backend.user.service.UserService;
import com.backend.utils.AjaxJson;
import com.backend.utils.minio.MinioUtils;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.mail.internet.MimeMessage;
import java.util.ArrayList;
import java.util.List;

/**
 * <p>
 * 前端控制器
 * </p>
 *
 * @author mumu
 * @since 2023-09-22
 */
@RestController
@RequestMapping("/user")
public class UserController {
    @Autowired
    UserService service;
    @Autowired
    JavaMailSender javaMailSender;
    @Autowired
    private MinioUtils minioUtilS;
    @Value("${minio.userPath}")
    private String userImgPath;

    @ApiOperation(value = "获取全部课程绩点", tags = "用户类")
    @GetMapping("/getAllScore")
    public AjaxJson getCourseScore() {
        String userId = StpUtil.getLoginIdAsString();
        if (userId == null) {
            return AjaxJson.getError("未登录");
        }
        return AjaxJson.getSuccessData(service.getAllScoreMap(userId));
    }

    @ApiOperation(value = "计算年级排名", tags = "用户类")
    @GetMapping("/countRank")
    public AjaxJson countRank(@RequestParam String userId) {
        User user = service.getUserById(userId);
        if (user == null) {
            return AjaxJson.getError("用户不存在！");
        }
        List<User> list = service.getRank(user.getUserMajor());
        for (int i = 0; i < list.size(); i++) {
            if (service.setUserRank(list.get(i).getUserId(), String.format("%d/%d", (i + 1), list.size())) != 1) {
                return AjaxJson.getError("出现未知错误！");
            }
        }
        return AjaxJson.getSuccessData(service.getUserById(userId).getUserRank());
    }

    @ApiOperation(value = "计算课程绩点", tags = "用户类")
    @GetMapping("/countScore")
    public AjaxJson countScore(@RequestParam String userId) {
        User user = service.getUserById(userId);
        if (user == null) {
            return AjaxJson.getError("用户不存在！");
        }
        Float score = service.countScore(userId);
        if (score == null) {
            score = 0f;
        }
        if (score.equals(user.getUserScore())) {
            return AjaxJson.getSuccessData(score);
        }
        if (service.setUserScore(userId, score) == 1) {
            return AjaxJson.getSuccessData(score);
        }
        return AjaxJson.getError("出现未知错误！");
    }

    @ApiOperation(value = "发送邮件", notes = "仅测试使用", tags = "测试类")
    @GetMapping("/test/send")//todo:delete this cell
    public String sendHtmlEmail() {
        try {
            MimeMessage mimeMessage = javaMailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, "utf-8");
            String verifyCode = "HIB1V7V";
            String htmlMsg = "<div style='background-color: #e1f5fe; padding: 20px;'>"
                    + "<h2>Welcome to SUSTech Campus!</h2>"
                    + "<p>Thank you for your interest. SUSTech Campus is a xxxxxxxxxxxx.</p>"//todo:change the html format
                    + "<p><strong>Below is your verification code:</strong></p>"
                    + "<div style='background-color: #ffffff;border: 2px solid #0277bd; padding: 5px; margin: 5px 0; text-align: center;'>"
                    + "<h3>" + verifyCode + "</h3>"
                    + "</div>"
                    + "<p>Please enter the above code to complete your registration.</p>"
                    + "<p>Explore our platform: <a href='https://pix2text.com'>SUSTech Campus</a></p>"
                    + "<p>If you didn't request this, please ignore this email.</p>"
                    + "</div>";
            helper.setText(htmlMsg, true); // 设置为true表示启用HTML格式的邮件
            helper.setTo("3096991519@qq.com");
            helper.setSubject("SUSTech Campus Verification Code");
            helper.setFrom("resetpassword_se@foxmail.com");

            javaMailSender.send(mimeMessage);
        } catch (Exception e) {
            e.printStackTrace();
            return "send fail";
        }
        return "send success";
    }

    @ApiOperation(value = "更新专业", tags = "用户类")
    @GetMapping("/updateMajor")
    public AjaxJson updateMajor(String userId, @RequestParam String major) {
        if (userId == null)
            userId = (String) StpUtil.getLoginId();
        if (userId == null)
            return AjaxJson.getError("请先登录");
        return service.setUserMajor(userId, major);
    }

    @ApiOperation(value = "更新邮箱", tags = "用户类")
    @GetMapping("/updateMail")
    public AjaxJson updateMail(String userId, @RequestParam String mail) {
        if (userId == null)
            userId = (String) StpUtil.getLoginId();
        if (userId == null)
            return AjaxJson.getError("请先登录");
        return service.setUserMail(userId, mail);
    }

    @ApiOperation(value = "发送重置邮件", tags = "用户类")
    @GetMapping("/sendResetEmail")
    public AjaxJson sendResetEmail(@RequestParam String userId) {
        if (userId == null)
            userId = (String) StpUtil.getLoginId();
        if (userId == null)
            return AjaxJson.getError("请先登录");
        return service.resetPassword(userId);
    }

    @ApiOperation(value = "通过重置代码重置", tags = "用户类")
    @GetMapping("/setPassword")
    public AjaxJson setPassword(@RequestParam String code, String password) {
        return service.resetPassword(code, password);
    }

    @ApiOperation(value = "下载用户图片，id为空时下载当前用户头像", tags = "用户类")
    @GetMapping("/userImg/download")
    public AjaxJson download(String userId) {
        if (userId == null) {
            userId = (String) StpUtil.getLoginId();
        }
        if (userId == null)
            return AjaxJson.getError("请先登录");
        return AjaxJson.getSuccessData(minioUtilS.downloadBytes(String.format("%s.jpeg", userId), userImgPath));
    }

    @ApiOperation(value = "上传用户图片", tags = "用户类")
    @SaCheckLogin
    @PostMapping("/userImg/upload")
    public AjaxJson upload(MultipartFile file) {
        minioUtilS.upload_reduce(file, userImgPath, String.format("%s.jpeg", StpUtil.getLoginId()));
        return AjaxJson.getSuccess();
    }


    //- http://localhost:9090/user/login
    @ApiOperation(value = "登录", tags = "用户类")
    @GetMapping("/login")
    public AjaxJson login(@RequestParam String userId, String userPassword) {
        if (userId == null || userId.isEmpty())
            return AjaxJson.getError("id不能为空");
        if (!service.isUserIdExists(userId)) {
            return AjaxJson.get(501, "用户名不存在");
        } else if (!service.isUserIdExists(userId, userPassword)) {
            return AjaxJson.get(502, "用户名或密码错误");
        } else {
            StpUtil.login(userId);
            UserInfoDTO user = service.login(userId);
            return AjaxJson.getSuccessData(user);
//            return AjaxJson.getSuccess();
        }
    }

    @ApiOperation(value = "管理员登录", tags = "测试类")
    @GetMapping("/authorized")
    public AjaxJson authorize() {
        StpUtil.login(service.getUserId("admin"));
        return AjaxJson.getSuccess();
    }

    //- http://localhost:9090/user/logout
    @ApiOperation(value = "登出", tags = "用户类")
    @GetMapping("/logout")
    public AjaxJson logout() {
        StpUtil.logout();
        return AjaxJson.getSuccess();
    }

    //- http://localhost:9090/user/list
    @ApiOperation(value = "显示全部用户", tags = "管理员类")
    @SaCheckRole("admin")
    @GetMapping("/list")
    public AjaxJson full_list() {
        return AjaxJson.getSuccessData(service.selectList());
    }

    @ApiOperation(value = "修改密码", tags = "用户类")
    @SaCheckLogin
    @GetMapping("/changePassword")
    public AjaxJson changePassword(String userId, @RequestParam String password, @RequestParam String newPassword) {
        if (userId == null)
            userId = (String) StpUtil.getLoginId();
        if (userId == null)
            return AjaxJson.getError("请先登录");
        return service.changePassword(userId, password, newPassword);
    }

    //- http://localhost:9090/user/new
    @ApiOperation(value = "用户注册", tags = "用户类")
    @GetMapping("/new")
    public AjaxJson add_user(User user) {
        if (!service.isUserIdExists(user.getUserId())) {
            if (user.getUserMail() == null)
                user.setMail();
            if (service.save(user)) {
                return AjaxJson.getSuccess();
            }
            return AjaxJson.get(504, "注册时出现未知错误！");
        }
        return AjaxJson.get(503, "已存在！");

    }

    @ApiOperation(value = "检查是否登录", tags = "用户类")
    @SaCheckLogin
    @GetMapping("/isLogin")
    public AjaxJson isLogin() {
        return AjaxJson.getSuccessData(service.getUser((String) StpUtil.getLoginId()));
    }

    @ApiOperation(value = "查询用户名是否存在", tags = "用户类")
    @GetMapping("/username")
    public AjaxJson name(String userId, String userName) {
        if (userId == null && userName == null) {   // null null
            return AjaxJson.getError("请输入信息");
        } else if (userId == null) {    // null name
            userId = service.getUserId(userName);
            if (userId == null) {
                return AjaxJson.getError("用户名不存在");
            }
        } else if (userName != null) {  // id name
            String id = service.getUserId(userName);
            if (id == null) {
                return AjaxJson.getError("用户名不存在");
            } else if (!id.equals(userId)) {
                String msg = "用户名id和名字不匹配";
                if (service.isUserIdExists(userId)) {
                    msg += "，userId存在";
                } else {
                    msg += "，userId不存在";
                }
                if (service.isUserIdExists(id)) {
                    msg += "，userName存在";
                } else {
                    msg += "，userName不存在";
                }
                return AjaxJson.getError(msg);
            }
        }
        if (!service.isUserIdExists(userId)) {
            return AjaxJson.getError("用户名不存在");
        } else {
            return AjaxJson.getSuccess();
        }
    }

    @ApiOperation(value = "批量注册", tags = "管理员类")
    @SaCheckRole("admin")
    @GetMapping("/signupList")
    public AjaxJson signupList(@RequestParam List<String> UserId, @RequestParam List<String> UserName) {
        List<AjaxJson> rr = new ArrayList<>();
        if (UserId.size() != UserName.size())
            return AjaxJson.getError("姓名学号数量不匹配");
        for (int i = 0, userIdSize = UserId.size(); i < userIdSize; i++) {
            String id = UserId.get(i);
            String name = UserName.get(i);
            try {
                service.save(new User(id, name, String.valueOf(id)));
            } catch (Exception e) {
                rr.add(new AjaxJson(500, String.format("%s failed in sign in, caused by %s", id, e.getCause()), id, null));
                e.printStackTrace();
            }
        }
        if (rr.isEmpty()) {
            return AjaxJson.getSuccess("success!");
        } else {
            return new AjaxJson(500, "部分插入失败", rr, (long) rr.size());
        }
    }

    @ApiOperation(value = "批量删除", tags = "管理员类")
    @SaCheckRole("admin")
    @GetMapping("/deleteList")
    public AjaxJson deleteList(@RequestParam List<String> UserId) {
        List<AjaxJson> rr = new ArrayList<>();
        for (String id : UserId) {
            try {
                service.remove(new MPJLambdaWrapper<User>().eq(User::getUserId, id));
            } catch (Exception e) {
                rr.add(new AjaxJson(500, String.format("%s failed in delete, caused by %s", id, e.getCause()), id, null));
                e.printStackTrace();
            }
        }
        if (rr.isEmpty()) {
            return AjaxJson.getSuccess("success!");
        } else {
            return new AjaxJson(500, "部分删除失败", rr, (long) rr.size());
        }
    }


    @ApiOperation(value = "重置账户", tags = "管理员类")
    @SaCheckRole("admin")
    @GetMapping("/reset")
    public AjaxJson reset(User user) {
        return service.resetPassword(user);
    }

    @ApiOperation(value = "获取用户信息", tags = "用户类")
    @GetMapping("/info")
    public AjaxJson getUserInformation(String userId) {
        if (userId == null) {
            userId = (String) StpUtil.getLoginId();
        }
        if (userId == null)
            return AjaxJson.getError("请先登录");
        return service.getUserInformation(userId);
    }

    @ApiOperation(value = "获取用户个人信息", tags = "用户类")
    @SaCheckLogin
    @GetMapping("/self")
    public AjaxJson getUserSelfInformation() {
        String userId = (String) StpUtil.getLoginId();
        if (userId == null)
            return AjaxJson.getError("请先登录");
        return service.getUserSelfInformation(userId);
    }
}
