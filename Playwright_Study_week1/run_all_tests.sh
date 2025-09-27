#!/bin/bash
# =============================================================================
# 自动化测试执行脚本
# 功能：运行所有测试用例，生成Allure报告，并自动打开报告
# 作者：熊🐻来个🥬
# 日期：2025/1/16
# =============================================================================

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印分割线
print_separator() {
    echo "=============================================================================="
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖环境..."
    
    # 检查pytest
    if ! command -v pytest &> /dev/null; then
        log_error "pytest 未安装，请先安装: pip install pytest"
        exit 1
    fi
    
    # 检查allure
    if ! command -v allure &> /dev/null; then
        log_warning "allure 未安装，将跳过报告生成"
        log_warning "安装方法: brew install allure (macOS)"
        ALLURE_AVAILABLE=false
    else
        ALLURE_AVAILABLE=true
    fi
    
    log_success "依赖检查完成"
}

# 清理旧的测试结果
cleanup_old_results() {
    log_info "清理旧的测试结果..."
    
    # 清理allure结果
    if [ -d "allure-results" ]; then
        rm -rf allure-results
        log_info "已清理 allure-results 目录"
    fi
    
    # 清理allure报告
    if [ -d "allure-report" ]; then
        rm -rf allure-report
        log_info "已清理 allure-report 目录"
    fi
    
    # 清理截图
    if [ -d "screenshots" ]; then
        rm -rf screenshots
        log_info "已清理 screenshots 目录"
    fi
    
    # 清理录制视频
    if [ -d "test_recordings" ]; then
        rm -rf test_recordings
        log_info "已清理 test_recordings 目录"
    fi
    
    # 清理日志文件
    if [ -f "test_login.log" ]; then
        rm test_login.log
        log_info "已清理 test_login.log 文件"
    fi
    
    log_success "清理完成"
}

# 运行测试
run_tests() {
    log_info "开始运行测试用例..."
    print_separator
    
    # 创建必要的目录
    mkdir -p allure-results
    mkdir -p screenshots
    mkdir -p test_recordings
    
    # 运行测试的参数
    PYTEST_ARGS=(
        "-v"                          # 详细输出
        "-s"                          # 显示print输出
        "--tb=short"                  # 简短的错误回溯
        "--alluredir=allure-results"  # Allure结果目录
        "--capture=no"                # 不捕获输出
        "tests/"                      # 测试目录
    )
    
    # 执行测试
    if pytest "${PYTEST_ARGS[@]}"; then
        log_success "所有测试用例执行完成"
        TEST_PASSED=true
    else
        log_warning "部分测试用例执行失败，但继续生成报告"
        TEST_PASSED=false
    fi
    
    print_separator
}

# 生成Allure报告
generate_allure_report() {
    if [ "$ALLURE_AVAILABLE" = true ]; then
        log_info "生成Allure报告..."
        
        if [ -d "allure-results" ] && [ "$(ls -A allure-results)" ]; then
            # 生成报告
            allure generate allure-results -o allure-report --clean
            log_success "Allure报告生成完成"
            
            # 显示报告路径
            REPORT_PATH="$(pwd)/allure-report/index.html"
            log_info "报告路径: file://$REPORT_PATH"
            
            return 0
        else
            log_warning "没有找到测试结果，跳过报告生成"
            return 1
        fi
    else
        log_warning "Allure未安装，跳过报告生成"
        return 1
    fi
}

# 打开Allure报告
open_allure_report() {
    if [ "$ALLURE_AVAILABLE" = true ] && [ -d "allure-report" ]; then
        log_info "启动Allure服务器..."
        log_info "报告将在浏览器中自动打开"
        log_info "按 Ctrl+C 停止服务器"
        
        # 启动allure服务器
        allure serve allure-results
    fi
}

# 显示测试结果摘要
show_summary() {
    print_separator
    log_info "测试执行摘要:"
    
    # 显示测试结果
    if [ "$TEST_PASSED" = true ]; then
        log_success "✅ 所有测试用例通过"
    else
        log_warning "⚠️  部分测试用例失败"
    fi
    
    # 显示生成的文件
    echo ""
    log_info "生成的文件:"
    
    if [ -d "screenshots" ] && [ "$(ls -A screenshots 2>/dev/null)" ]; then
        SCREENSHOT_COUNT=$(ls screenshots/*.png 2>/dev/null | wc -l)
        echo "  📸 截图文件: $SCREENSHOT_COUNT 张 (screenshots/)"
    fi
    
    if [ -d "test_recordings" ] && [ "$(ls -A test_recordings 2>/dev/null)" ]; then
        VIDEO_COUNT=$(ls test_recordings/*.webm 2>/dev/null | wc -l)
        echo "  🎬 录制视频: $VIDEO_COUNT 个 (test_recordings/)"
    fi
    
    if [ -f "test_login.log" ]; then
        echo "  📝 测试日志: test_login.log"
    fi
    
    if [ -d "allure-report" ]; then
        echo "  📊 Allure报告: allure-report/index.html"
    fi
    
    print_separator
}

# 主函数
main() {
    # 切换到脚本所在目录
    cd "$(dirname "$0")"
    
    print_separator
    log_info "🚀 开始执行自动化测试"
    log_info "当前目录: $(pwd)"
    print_separator
    
    # 检查依赖
    check_dependencies
    
    # 清理旧结果
    cleanup_old_results
    
    # 运行测试
    run_tests
    
    # 生成报告
    if generate_allure_report; then
        show_summary
        
        # 询问是否打开报告
        echo ""
        read -p "是否打开Allure报告? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open_allure_report
        else
            log_info "可以稍后运行以下命令查看报告:"
            log_info "allure serve allure-results"
        fi
    else
        show_summary
    fi
    
    log_success "🎉 测试执行完成!"
}

# 捕获中断信号
trap 'log_warning "测试被用户中断"; exit 1' INT

# 执行主函数
main "$@"