package com.backend.user.service.impl;

import com.backend.user.entity.Permission;
import com.backend.user.mapper.PermissionMapper;
import com.backend.user.service.PermissionService;
import com.backend.user.service.UserService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * <p>
 * 服务实现类
 * </p>
 *
 * @author mumu
 * @since 2023-10-15
 */
@Service
@Transactional
public class PermissionServiceImpl extends ServiceImpl<PermissionMapper, Permission> implements PermissionService {
    @Autowired
    PermissionMapper mapper;
    @Autowired
    UserService userService;

    @Override
    public boolean insertPermission(String id, List<Integer> permission) {
        boolean tt = true;
        for (Integer a : permission) {
            mapper.insert(new Permission(id, a));
        }
        return tt;
    }

    @Override
    public boolean deletePermission(String id, List<Integer> permission) {
        boolean tt = true;
        for (Integer a : permission) {
            mapper.delete(new MPJLambdaWrapper<Permission>().eq(Permission::getPermissionId, a).eq(Permission::getUserId, id));
        }
        return tt;
    }
}
