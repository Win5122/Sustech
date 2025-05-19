package com.backend.user.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.io.Serial;
import java.io.Serializable;

/**
 * <p>
 *
 * </p>
 *
 * @author mumu
 * @since 2023-10-15
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@EqualsAndHashCode(callSuper = false)
public class Permission implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;

    private String userId;

    private Integer roleId;

    @TableId(value = "permission_id", type = IdType.AUTO)
    private Integer permissionId;

    public Permission(String userId, Integer roleId) {
        this.userId = userId;
        this.roleId = roleId;
    }

}
