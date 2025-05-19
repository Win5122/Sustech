package com.backend.user.entity;

import lombok.*;

import java.io.Serial;
import java.io.Serializable;

/**
 * <p>
 *
 * </p>
 *
 * @author mumu
 * @since 2023-09-22
 */
@Data
@ToString
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = false)
public class User implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;

    private String userId;

    private String userName;

    private String userPassword;

    /**
     * 本/硕/博
     */
    private String userType;

    private String userImg;

    private String uerGender;

    private String userBirthday;

    private String userPhone;

    private String userMail;

    private String userMajor;

    private String userCome;

    private Float userScore;

    private String userRank;

    private Integer userValid;

    public User(String userId, String userName, String userPassword) {
        this.userId = userId;
        this.userName = userName;
        this.userPassword = userPassword;
        this.userMail = userId + "@mail.sustech.edu.cn";
        this.userMajor = "通识通修";
    }

    public void setMail() {
        this.userMail = this.userId + "@mail.sustech.edu.cn";
    }

    public void setMajor() {
        this.userMajor = "通识通修";
    }
}
