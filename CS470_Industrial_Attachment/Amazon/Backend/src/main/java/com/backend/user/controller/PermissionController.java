package com.backend.user.controller;


import com.backend.user.service.PermissionService;
import com.backend.utils.AjaxJson;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * <p>
 * 前端控制器
 * </p>
 *
 * @author mumu
 * @since 2023-10-15
 */
@RestController
@RequestMapping("/permission")
public class PermissionController {
    @Autowired
    PermissionService service;

    //    @SaCheckRole("admin")
    @ApiOperation(value = "设置权限", tags = "管理员类")
    @GetMapping("/givePower")
    public AjaxJson powerList(@RequestParam List<String> UserId, @RequestParam List<Integer> UserPower) {
        List<AjaxJson> rr = new ArrayList<>();
        for (String id : UserId) {
            try {
                service.insertPermission(id, UserPower);
            } catch (Exception e) {
                rr.add(new AjaxJson(500, String.format("%s failed in sign in, caused by %s", id, e.getCause()), id, null));
                e.printStackTrace();
            }
        }
        if (rr.isEmpty()) {
            return AjaxJson.getSuccess();
        } else {
            return new AjaxJson(500, "部分权限更新失败", rr, (long) rr.size());
        }
    }

    @ApiOperation(value = "设置权限", tags = "管理员类")
    @GetMapping("/removePower")
    public AjaxJson deletePower(@RequestParam String UserId, @RequestParam Integer UserPower) {
        service.deletePermission(UserId, Collections.singletonList(UserPower));
        return AjaxJson.getSuccess();
    }

    @ApiOperation(value = "设置权限", tags = "管理员类")
    @GetMapping("/addPower")
    public AjaxJson addPower(@RequestParam String UserId, @RequestParam Integer UserPower) {
        service.insertPermission(UserId, Collections.singletonList(UserPower));
        return AjaxJson.getSuccess();
    }
}



