package com.logitics.erp.leavepolicy.repository;

import com.logitics.erp.leavepolicy.entity.LeavePolicy;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LeavePolicyRepository extends JpaRepository<LeavePolicy, Long> {
}
