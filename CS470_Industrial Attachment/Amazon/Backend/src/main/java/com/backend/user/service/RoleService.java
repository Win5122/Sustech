package com.backend.user.service;

import com.backend.user.entity.Role;
import com.baomidou.mybatisplus.extension.service.IService;
import org.springframework.transaction.annotation.Transactional;

/**
 * <p>
 * 服务类
 * </p>
 *
 * @author mumu
 * @since 2023-10-14
 */
@Transactional
public interface RoleService extends IService<Role> {

}
