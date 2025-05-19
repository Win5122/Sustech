package com.backend.user.entity.dto;

import lombok.Data;
import lombok.ToString;

import java.io.Serializable;

@Data
@ToString
public class UserMajorDTO implements Serializable {
    // user
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

    private String userCome;

    private Float userScore;

    private String userRank;

    private Integer userValid;

    // major
    private String majorType;

    private String majorName;
}
