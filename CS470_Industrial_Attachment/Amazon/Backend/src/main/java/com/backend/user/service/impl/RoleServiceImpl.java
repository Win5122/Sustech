package com.backend.user.service.impl;

import com.backend.user.entity.Role;
import com.backend.user.mapper.RoleMapper;
import com.backend.user.service.RoleService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * <p>
 * 服务实现类
 * </p>
 *
 * @author mumu
 * @since 2023-10-14
 */
@Service
@Transactional
public class RoleServiceImpl extends ServiceImpl<RoleMapper, Role> implements RoleService {
    @Autowired
    RoleMapper mapper;

}
